import cv2
import numpy as np
import mxnet as mx
import mxnet.ndarray as nd
from mxnet import gluon
from sklearn.preprocessing import normalize
from .face_preprocess import preprocess

class ArcFace:

    def __init__(self, model_path, gpuid, image_size=(112, 112)):
        self.model_path = model_path
        self.ctx = mx.gpu(gpuid) if gpuid >= 0 else mx.cpu()
        self.image_size = image_size
        self.model = self._get_model(self.ctx, self.image_size)

    def _get_model(self, ctx, image_size):
        sym, arg_params, aux_params = mx.model.load_checkpoint(self.model_path, 0)
        all_layers = sym.get_internals()
        sym = all_layers['fc1'+'_output']

        model = mx.mod.Module(symbol=sym, context=ctx, label_names = None)
        model.bind(data_shapes=[('data', (1, 3, image_size[0], image_size[1]))])
        model.set_params(arg_params, aux_params)
        return model

    def _img_to_mxnd(self, img):
        img = mx.nd.array(img)
        img = mx.image.imresize(img, 112, 112)
        img = img.transpose((2, 0, 1))  # Channel first
        # img = img.expand_dims(axis=0)  # batchify
        img = img.astype('float32')  # for gpu context


        return img

    def image_preprocess(self,
                         img,
                         bbox=None,
                         landmark=None,
                         image_size='112,112'):
        # input: rgb
        bbox = bbox[0:4]
        img = img[..., ::-1]
        n_img = preprocess(img, bbox[0], landmark, image_size='112,112')
        n_img = cv2.cvtColor(n_img, cv2.COLOR_BGR2RGB)
        return n_img

    def get_embedding(self, img, s=1):
        # img: cropped + aligned face image (bgr)
        embedding = None
        img_flip = cv2.flip(img, 1)

        img = self._img_to_mxnd(img)
        img_flip = self._img_to_mxnd(img_flip)

        image_tensor = [img, img_flip]
        stacked_tensor = mx.nd.zeros((2, 3, 112, 112))
        mx.nd.stack(*image_tensor, axis=0, out=stacked_tensor)

        db_1 = mx.io.DataBatch(data=(stacked_tensor,))
        embedding_1 = self.model.forward(db_1, is_train=False)
        embedding_1 = self.model.get_outputs()[0].asnumpy()

        embedding, embedding_2 = np.split(embedding_1, 2)

        embedding += embedding_2
        result = normalize(embedding).flatten() * s

        return result

    def get_multi_embedding(self, img_list, s=1):
        # img: cropped + aligned face image (bgr)
        embedding = None
        result = []
        image_tensor = []
        # print('============= start ================')
        for img in img_list:
            # print("Image shape", img.shape)
            img_flip = cv2.flip(img, 1)

            img = self._img_to_mxnd(img)
            img_flip = self._img_to_mxnd(img_flip)

            image_tensor.append(img)
            image_tensor.append(img_flip)
            
        stacked_tensor = mx.nd.zeros((len(img_list)*2, 3, 112, 112))
        mx.nd.stack(*image_tensor, axis=0, out=stacked_tensor)
        db_1 = mx.io.DataBatch(data=(stacked_tensor,))

        embedding = self.model.forward(db_1, is_train=False)
        embedding = self.model.get_outputs()[0].asnumpy()
        
        for i in range(0,len(embedding),2):
            embedding_result = embedding[i] + embedding[i+1]
            embedding_result = embedding_result.reshape(1,512)
            embedding_result = normalize(embedding_result).flatten() * s
            result.append(embedding_result)
        # print('============= end ================')
        return result
