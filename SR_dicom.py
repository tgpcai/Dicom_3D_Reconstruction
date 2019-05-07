# 抽取轮廓(等值面)的操作对象是标量数据。
# 其思想是：将数据集中标量值等于某一指定恒量值的部分提取出来。对于3D的数据集而言，产生的是一个等值面；对于2D的数据集而言，产生的是一个等值线。
# 其典型的应用有气象图中的等温线、地形图中的等高线。对于医学数据而言，不同的标量值代表的是人体的不同部分，因而可以分别提取出人的皮肤或骨头。
# 抽取轮廓的功能是由一个过滤器实现的，如vtkContourFilter、vtkMarchingCubes。vtkContourFilter可以接受任意数据集类型作为输入，因而具有 一般性。
# 使用vtkContourFilter 时，除了需要设置输入数据集外，还需要指定一个或多个用于抽取的标量值。可用如下两种方法进行设置。
#
# 使用方法SetValue()逐个设置抽取值。该方法有个两个参数：第一个参数是抽取值的索引号，表示第几个 抽取值。索引号从0开始计数；第二个参数就是指定的抽取值。
# 使用方法GenerateValues()自动产生一系列抽取值。该方法有三个参数：第一个参数是抽取值的个数，后面两个参数是抽取值的取值范围。

# coding=utf-8
import vtk

# source—filter——mapper——actor——render——renderwindow——interactor
aRenderer = vtk.vtkRenderer()  # 渲染器
renWin = vtk.vtkRenderWindow()  # 渲染窗口,创建窗口
renWin.AddRenderer(aRenderer)  # 渲染窗口
# renWin.Render()
iren = vtk.vtkRenderWindowInteractor()  # 窗口交互
iren.SetRenderWindow(renWin)

# The following reader is used to read a series of 2D slices(images)
# that compose the volume.Theslicedimensions are set, and the
#  pixel spacing.The data Endianness must also be specified.The reader
#  uses the FilePrefix in combination with the slice number to construct
# filenames using the format FilePrefix. % d.(In this case the FilePrefix
# is the root name of the file.

v16 = vtk.vtkDICOMImageReader()
# v16.SetDirectoryName('D:/dicom_image/V')
v16.SetDirectoryName('D:/dicom_image/vtkDicomRender-master/sample')



# An isosurface, or contour value of 500 is known to correspond to the
# skin of the patient.Once generated, a vtkPolyDataNormals filter is
# used to create normals for smooth surface shading during rendering.
skinExtractor = vtk.vtkContourFilter()
skinExtractor.SetInputConnection(v16.GetOutputPort())
skinExtractor.SetValue(0, -10)
# skinExtractor.GenerateValues(2, 100, 110)
skinNormals = vtk.vtkPolyDataNormals()
skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
skinNormals.SetFeatureAngle(60.0)
skinMapper = vtk.vtkPolyDataMapper()  # 映射器
skinMapper.SetInputConnection(skinNormals.GetOutputPort())
skinMapper.ScalarVisibilityOff()

skin = vtk.vtkActor()
# 设置颜色RGB颜色系统就是由三个颜色分量：红色(R)、绿色(G)和蓝色(B)的组合表示，
# 在VTK里这三个分量的取值都是从0到1，(0, 0, 0)表示黑色，(1, 1, 1)表示白色。
#  vtkProperty::SetColor(r,g, b)采用的就是RGB颜色系统设置颜色属性值。
#skin.GetProperty().SetColor(0, 0, 1)
skin.SetMapper(skinMapper)

skin.GetProperty().SetDiffuseColor(1, .49, .25)

skin.GetProperty().SetSpecular(.5)

skin.GetProperty().SetSpecularPower(20)

# skin.GetProperty().SetRepresentationToSurface()
# 构建图形的方框
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(v16.GetOutputPort())
mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())
outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(0, 0, 0)

# 构建舞台的相机
aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(0, 1, 0)
aCamera.SetFocalPoint(0, 0, 0)
aCamera.ComputeViewPlaneNormal()

# Actors are added to the renderer.An initial camera view is created.
# The Dolly() method moves the camera towards the Focal　Point,
# thereby enlarging the image.
aRenderer.AddActor(outline)
aRenderer.AddActor(skin)
aRenderer.SetActiveCamera(aCamera)
# 将相机的焦点移动至中央，The camera will reposition itself to view the center point of the actors,
# and move along its initial view plane normal
aRenderer.ResetCamera()
# aCamera.Dolly(1.5)
# aCamera.Roll(180)
# aCamera.Yaw(60)

aRenderer.SetBackground(250, 250, 250)
# renWin.SetSize(640, 480)
# 该方法是从vtkRenderWindow的父类vtkWindow继承过来的，用于设置窗口的大小，以像素为单位。
renWin.SetSize(500, 500)
aRenderer.ResetCameraClippingRange()

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Start()