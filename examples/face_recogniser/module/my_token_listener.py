import os.path
from os import listdir
from os.path import isfile, join
from typing import List, Tuple
import face_recognition
from matplotlib import pyplot, patches
from PIL import Image
import numpy as np
from balticlsc.computation_module.api_access.job_controller import init_job_controller, TokenListener
from balticlsc.computation_module.baltic_lsc.data_handler import IDataHandler
from balticlsc.computation_module.baltic_lsc.job_registry import IJobRegistry
from balticlsc.computation_module.data_model.messages import Status
from balticlsc.computation_module.utils.logger import logger


class MyTokenListener(TokenListener):

    def __init__(self, registry: IJobRegistry, data: IDataHandler):
        super().__init__(registry, data)

    def data_received(self, pin_name: str):
        # Place your code here:
        pass

    def optional_data_received(self, pin_name: str):
        # Place your code here:
        pass

    def data_ready(self):
        # Place your code here:
        pass

    def data_complete(self):
        self._registry.set_status(Status.WORKING)
        filepath = self._data.obtain_data_item('Input')
        filename = os.path.basename(filepath)

        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            msg = 'wrong format of the file "' + filename + '", omitting'
            logger.warning(msg)
            raise ValueError(msg)

        # Mark faces and save the image
        image = np.array(Image.open(filepath))
        im = Image.fromarray(image)
        im.save(filepath)
        height: int = image.shape[0]
        width: int = image.shape[1]
        dpi: int = 100
        faces_coords: List[Tuple[int]] = face_recognition.face_locations(image)
        figure = pyplot.figure(frameon=False, dpi=dpi)
        figure.set_size_inches(width / dpi, height / dpi)
        ax = pyplot.Axes(figure, [0., 0., 1., 1.])
        ax.set_axis_off()
        figure.add_axes(ax)
        ax.imshow(image)
        logger.info('adding ' + str(len(faces_coords)) + ' faces to image "' + filename + '"')
        fig = pyplot.gcf()
        fig.savefig(fname=filepath, dpi=dpi, bbox_inches='tight')

        for index in range(len(faces_coords)):
            x_start = faces_coords[index][3]
            y_start = faces_coords[index][0]
            x_width = (faces_coords[index][1] - faces_coords[index][3])
            y_height = (faces_coords[index][2] - faces_coords[index][0])
            rect = patches.Rectangle((x_start, y_start), x_width, y_height,
                                     edgecolor='r', facecolor="none")
            ax.add_patch(rect)

        pyplot.savefig(fname=filepath, dpi=dpi, bbox_inches='tight')
        pyplot.close()
        self._data.send_data_item('Output', filepath, True)
        self._data.finish_processing()


app = init_job_controller(MyTokenListener)
