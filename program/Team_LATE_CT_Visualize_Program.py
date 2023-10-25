import sys
import io
import numpy as np
import SimpleITK as sitk
import itk
import cv2
import matplotlib.pyplot as plt
import vtkmodules.all as vtk
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QGridLayout, QLabel, QSlider, QPushButton, QFileDialog, QMainWindow, QApplication, QCheckBox,QFileDialog 
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from scipy.ndimage import zoom

def vtk_image_to_numpy(image):
    width, height, _ = image.GetDimensions()
    vtk_data = image.GetPointData().GetScalars()
    numpy_array = np.frombuffer(vtk_data, dtype=np.uint8)
    numpy_array = numpy_array.reshape(height, width, -1)
    return numpy_array

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.threshold = 100
        self.rendered_3d_image = None
        self.setWindowTitle("PNU TEAM LATE")
        self.setGeometry(100, 100, 1200, 800)

        
        top_layout = QVBoxLayout()
        top_widget = QWidget(self)
        top_widget.setLayout(top_layout)

        button_layout = QHBoxLayout()

        
        self.nii_file_button = QPushButton("Select CT File")
        self.nii_file_button.clicked.connect(self.open_nifti_file_dialog)
        button_layout.addWidget(self.nii_file_button)

        
        self.label_file_button = QPushButton("Select Label File")
        self.label_file_button.clicked.connect(self.open_label_file_dialog)
        button_layout.addWidget(self.label_file_button)

        top_layout.addLayout(button_layout)

        self.image_grid = QGridLayout()
        self.image_labels = []
        self.sliders = []
        self.img_data = None  
        self.label_data = None  
        self.checkboxes = []  
        for i in range(3):
           
            image_label = QLabel(self)
            image_label.setFixedSize(400, 400)
            image_label.setScaledContents(True) 
            self.image_labels.append(image_label)
            self.image_grid.addWidget(image_label, 0, i)
            image_label.setStyleSheet("background-color: black;")
            
            
           
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(0)  
            slider.setFixedWidth(400) 
            slider.valueChanged.connect(lambda value, idx=i: self.update_slice(value, idx))
            self.sliders.append(slider)
            self.image_grid.addWidget(slider, 1, i)

        top_layout.addLayout(self.image_grid)

       
        bottom_layout = QVBoxLayout()
        bottom_widget = QWidget(self)
        bottom_widget.setLayout(bottom_layout)

       
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        bottom_layout.addWidget(self.vtk_widget)

        
        button_layout_below_viewer = QHBoxLayout()
        bottom_layout.addLayout(button_layout_below_viewer)

        organs = ["Liver", "Kidney", "Spleen", "Pancreas"]
        i=0
        for organ in organs:
            
            checkbox = QCheckBox(organ)
            checkbox.setChecked(True)  
            checkbox.stateChanged.connect(lambda state, index=i: self.toggle_function(index, state))
            self.checkboxes.append(checkbox)
            button_layout_below_viewer.addWidget(checkbox)
            i=i+1

        self.bounding_box_checkbox = QCheckBox("BoundingBox")
        self.bounding_box_checkbox.setChecked(False)  
        self.bounding_box_checkbox.stateChanged.connect(self.toggle_bounding_box)
        button_layout_below_viewer.addWidget(self.bounding_box_checkbox)
        

        button_layout_below_viewer = QHBoxLayout()
        bottom_layout.addLayout(button_layout_below_viewer)

        self.add_button = QPushButton("SHOW 3D MODEL")
        self.add_button.clicked.connect(self.add_button_clicked)
        button_layout_below_viewer.addWidget(self.add_button)


        self.save_button = QPushButton("Save Images")
        self.save_button.clicked.connect(self.save_images)
        button_layout_below_viewer.addWidget(self.save_button)
    
      
        self.functions_enabled = [True] * 4
        
       
        self.img_data = None
        self.axial_aspect_ratio = 1.0  

        
        central_layout = QVBoxLayout()
        central_widget = QWidget(self)
        central_layout.addWidget(top_widget)
        central_layout.addWidget(bottom_widget)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        
        self.functions_enabled = [True] * 4

        
        self.volume_property = None
        self.opacity_transfer_function = None
        self.color_transfer_function = None
        self.label_file_path = None 

   
    def open_nifti_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "NIfTI 파일 선택", "", "NIfTI Files (*.nii.gz);;All Files (*)", options=options)

        if file_name:
            self.load_nifti_image(file_name)

    
    def open_label_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Label 선택", "", "NIfTI Files (*.nii.gz);;All Files (*)", options=options)

        if file_name:
            self.load_label_image(file_name)

    
    def load_nifti_image(self, file_name):
        itk_image = itk.imread(file_name)
        self.img_data = itk.array_from_image(itk_image)
        self.sliders[0].setMaximum(self.img_data.shape[0] - 1)  
        self.sliders[1].setMaximum(self.img_data.shape[1] - 1)  
        self.sliders[2].setMaximum(self.img_data.shape[2] - 1)  

       
        self.axial_aspect_ratio = itk_image.GetSpacing()[2] / itk_image.GetSpacing()[1]

        self.update_all_slices()

    
    def load_label_image(self, file_name):
        itk_image = itk.imread(file_name)
        self.label_data = itk.array_from_image(itk_image)

        self.update_all_slices()
        self.label_file_path = file_name 
        self.add_button.setEnabled(True)

   
    def update_all_slices(self):
        for i in range(3):
            self.update_slice(self.sliders[i].value(), i)

    def toggle_bounding_box(self, state):
        for i in range(3):
            if self.img_data is not None and self.label_data is not None:
                self.update_slice(self.sliders[i].value(), i)

    def toggle_function(self, organ_index, state):
        if organ_index >= 0 and organ_index < len(self.checkboxes):
            if self.label_file_path is None:
                return
            else:
                self.functions_enabled[organ_index] = state == Qt.Checked

            
            if self.functions_enabled[organ_index]:
                self.opacity_transfer_function.AddPoint(organ_index+1, 0.1)  
            else:
                self.opacity_transfer_function.AddPoint(organ_index+1, 0.0)  

    
    def update_slice(self, value, index):
        if self.img_data is None:
            return

        
        if index == 0:  # Axial
            slice_data = np.rot90(self.img_data[value, :,:], k=2)
        elif index == 1:  # Sagittal
            slice_data = np.rot90(self.img_data[:, value, :], k=2)
        else:  # Coronal
            slice_data = np.rot90(self.img_data[:, :, value], k=2)

       
        if self.label_data is not None:
            
            if index == 0:  # Axial
                label_slice = np.rot90(self.label_data[value, :, :], k=2)
            elif index == 1:  # Sagittal
                label_slice = np.rot90(self.label_data[:, value, :], k=2)
            else:  # Coronal
                label_slice = np.rot90(self.label_data[:, :, value], k=2)

            plt.imshow(slice_data, cmap="gray")
            plt.imshow(label_slice, cmap="hot", alpha=0.45)

            
            if self.bounding_box_checkbox.isChecked():
                contours, _ = cv2.findContours(label_slice.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    plt.gca().add_patch(plt.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none'))

        else:
            plt.imshow(slice_data, cmap="gray")

        plt.axis('off')

        buffer = io.BytesIO()
        plt.savefig(buffer, bbox_inches='tight', format='png', dpi=100)
        buffer.seek(0)

        img = QImage.fromData(buffer.getvalue(), format='png')
        pixmap = QPixmap.fromImage(img)

       
        width, height = self.image_labels[index].width(), self.image_labels[index].height()
        new_height = int(width / self.axial_aspect_ratio)
        pixmap = pixmap.scaled(width, 300, Qt.KeepAspectRatio)

        self.image_labels[index].setPixmap(pixmap)

        plt.close()

    
    def add_button_clicked(self):
        if self.label_file_path:

            reader = vtk.vtkNIFTIImageReader()
            reader.SetFileName(self.label_file_path)
            reader.Update()

          
            image_data = reader.GetOutput()

          
            render_window = self.vtk_widget.GetRenderWindow()
            render_view = render_window.GetInteractor()


          
            renderer = vtk.vtkRenderer()
            render_window.AddRenderer(renderer)

        
            min_label = 1
            max_label = 5  

            
            organ_label_data = vtk.vtkImageData()
            organ_label_data.ShallowCopy(image_data)

            
            organ_label_array = organ_label_data.GetPointData().GetScalars()

            for i in range(organ_label_array.GetNumberOfTuples()):
                label = organ_label_array.GetTuple1(i)
                if label < min_label or label > max_label:
                    organ_label_array.SetTuple1(i, 0)

            organ_label_data.GetPointData().Modified()
            organ_label_data.GetPointData().Update()

            volume_mapper = vtk.vtkSmartVolumeMapper()
            volume_mapper.SetBlendModeToComposite()
            volume_mapper.SetInputData(organ_label_data)

            
            self.volume_property = vtk.vtkVolumeProperty()
            self.volume_property.ShadeOff()
            self.volume_property.SetInterpolationTypeToLinear()

            
            self.color_transfer_function = vtk.vtkColorTransferFunction()  
            self.color_transfer_function.AddRGBPoint(0, 1.0, 1.0, 1.0)  # 레이블 0의 색상                
            self.color_transfer_function.AddRGBPoint(1, 1.0, 0.0, 0.0)  # 레이블 1의 색상 
            self.color_transfer_function.AddRGBPoint(2, 0.0, 1.0, 0.0)  # 레이블 1의 색상 
            self.color_transfer_function.AddRGBPoint(3, 0.0, 0.0, 1.0)  # 레이블 2의 색상 
            self.color_transfer_function.AddRGBPoint(4, 1.0, 1.0, 0.0)  # 레이블 3의 색상 
            self.volume_property.SetColor(self.color_transfer_function)

            self.opacity_transfer_function = vtk.vtkPiecewiseFunction()      
            self.opacity_transfer_function.AddPoint(0, 0.0)  # 레이블 0의 불투명도            
            self.opacity_transfer_function.AddPoint(1, 0.1)  # 레이블 1의 불투명도
            self.opacity_transfer_function.AddPoint(2, 0.1)  # 레이블 2의 불투명도
            self.opacity_transfer_function.AddPoint(3, 0.1)  # 레이블 3의 불투명도
            self.opacity_transfer_function.AddPoint(4, 0.1)  # 레이블 4의 불투명도
            self.volume_property.SetScalarOpacity(self.opacity_transfer_function)

            
            volume = vtk.vtkVolume()
            volume.SetMapper(volume_mapper)
            volume.SetProperty(self.volume_property)

            renderer.AddVolume(volume)

            
            volume_mapper.SetSampleDistance(0.1)  

            renderer.ResetCamera()
            render_window.Render()

            window_to_image_filter = vtk.vtkWindowToImageFilter()
            window_to_image_filter.SetInput(render_window)
            window_to_image_filter.Update()
            self.rendered_3d_image = window_to_image_filter.GetOutput()

            render_view.Start()           


        else:
            print("3D모델링 버튼이 클릭되었습니다. 그러나 선택한 파일이 없습니다.")



    def save_images(self):
        if self.img_data is not None and self.label_data is not None:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Images", "", "PNG Files (*.png);;All Files (*)", options=options)

            if file_path:
            
                axial_slice = self.sliders[0].value()
                sagittal_slice = self.sliders[1].value()
                coronal_slice = self.sliders[2].value()

            
                axial_image = np.rot90(self.img_data[axial_slice, :, :], k=2)
                sagittal_image = np.rot90(self.img_data[:, sagittal_slice, :], k=2)
                coronal_image = np.rot90(self.img_data[:, :, coronal_slice], k=2)

            
                axial_label_image = np.rot90(self.label_data[axial_slice, :, :], k=2)
                sagittal_label_image = np.rot90(self.label_data[:, sagittal_slice, :], k=2)
                coronal_label_image = np.rot90(self.label_data[:, :, coronal_slice], k=2)

            
                fig = plt.figure(figsize=(50,50))


           
                ax1 = plt.subplot2grid((3, 3), (0, 0))
                ax2 = plt.subplot2grid((3, 3), (0, 1))
                ax3 = plt.subplot2grid((3, 3), (0, 2))

                new_width = 250  # 새로운 가로 크기
                new_height =250   # 새로운 세로 크기
                axial_image_resized = cv2.resize(axial_image, (new_width, new_height))
                sagittal_image_resized = cv2.resize(sagittal_image, (new_width, new_height))
                coronal_image_resized = cv2.resize(coronal_image, (new_width, new_height))
       
                axial_label_resized = cv2.resize(axial_label_image, (new_width, new_height))
                sagittal_label_resized = cv2.resize(sagittal_label_image, (new_width, new_height))
                coronal_label_resized = cv2.resize(coronal_label_image, (new_width, new_height))



                ax1.imshow(axial_image_resized, cmap="gray")
                ax1.set_title("Axial Slice",fontsize=50)
                ax1.set_axis_off()

                ax2.imshow(sagittal_image_resized, cmap="gray")
                ax2.set_title("Sagittal Slice",fontsize=50)
                ax2.set_axis_off()

                ax3.imshow(coronal_image_resized, cmap="gray")
                ax3.set_title("Coronal Slice",fontsize=50)
                ax3.set_axis_off()

           
                ax4 = plt.subplot2grid((3, 3), (1, 0))
                ax5 = plt.subplot2grid((3, 3), (1, 1))
                ax6 = plt.subplot2grid((3, 3), (1, 2))

                ax4.imshow(axial_image_resized, cmap="gray")
                ax4.imshow(axial_label_resized, cmap="hot", alpha=0.45)
                ax4.set_title("Axial Slice with Mask",fontsize=50)                
                ax4.set_axis_off()

                ax5.imshow(sagittal_image_resized, cmap="gray")
                ax5.imshow(sagittal_label_resized, cmap="hot", alpha=0.45)
                ax5.set_title("Sagittal Slice with Mask",fontsize=50)                     
                ax5.set_axis_off()


                ax6.imshow(coronal_image_resized, cmap="gray")
                ax6.imshow(coronal_label_resized, cmap="hot", alpha=0.45)
                ax6.set_title("Coronal Slice with Mask",fontsize=50)                  
                ax6.set_axis_off()

                if self.rendered_3d_image:
                    render_window = self.vtk_widget.GetRenderWindow()
                    render_window.Render()





                    window_to_image_filter = vtk.vtkWindowToImageFilter()
                    window_to_image_filter.SetInput(render_window)
                    window_to_image_filter.Update()
                    captured_image = window_to_image_filter.GetOutput()
                    captured_image_np = vtk_image_to_numpy(captured_image)
                    captured_image_np = np.flipud(captured_image_np)
                    ax7 = plt.subplot2grid((3, 3), (2, 0), colspan=3)
                    ax7.set_title("3D Image",fontsize=50)    
                    ax7.imshow(captured_image_np)
                    ax7.set_axis_off()

           
                fig.savefig(file_path, bbox_inches='tight', format='png', dpi=100)
                plt.close(fig)
                print(f"Images saved as {file_path}")
            else:
                print("No file path selected for saving.") 
        else:
            print("No NIfTI image or label image loaded to save.")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())
