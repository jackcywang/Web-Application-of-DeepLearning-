import os.path
from class_id import label_id_names
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
from PIL import Image
import torchvision.transforms as T
from torchvision import transforms
from model import Dense201
import torch.nn.functional as F
import torch
# import pickle

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

# netparams = 'train.params'
# ids_synsets_name = 'ids_synsets'

# f = open(ids_synsets_name,'rb')
# ids_synsets = pickle.load(f)
# f.close()


# PP = Pre(netparams,ids_synsets[1],1)

model = Dense201()
model.load_state_dict(torch.load('./weights/model_bestbestacc.pth',map_location='cpu'))
model.eval()



trans=T.Compose([
            transforms.Scale(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
        ])


def RemoveFile(dirhname):
    for root, dirs, files in os.walk(dirhname):
        for name in files:
            os.remove(os.path.join(root, name))

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',imagename="",classname="")

class Update_Image(tornado.web.RequestHandler):
    def post(self):
        RemoveFile("./static/image/")
        try:
            img = self.request.files['file'][0]
            f = open("./static/image/"+img['filename'],'wb')
            f.write(img['body'])
            f.close()
            # classname = PP.PreName("./static/image/"+img['filename']).lower()
            img_path = "./static/image/"+img['filename']
            image = Image.open(img_path)
            image = trans(image)
            image = image.unsqueeze(0)
            with torch.no_grad():
                pred_score = model(image)
                pred_score = F.softmax(pred_score.data,dim=1)
                if pred_score is not None:
                        pred_label = torch.argsort(pred_score[0], descending=True)[:1][0].item()
                        result = {'result': label_id_names[str(pred_label)]}
                else:
                    result = {'result': 'predict score is None'}

            classname = result['result']
            # classname = None
            self.render('index.html',imagename="./static/image/"+img['filename'],classname = classname)
        except KeyError:
            print("Please select a image file!!!")

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/Updata_Image', Update_Image)],
        template_path=os.path.join(os.path.dirname(__file__), "./templates"),
        static_path=os.path.join(os.path.dirname(__file__),'./static'),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()