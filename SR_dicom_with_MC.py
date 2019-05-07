import vtk
# source->filter(MC算法)->mapper->actor->render->renderwindow->interactor

# 读取Dicom数据，对应source
v16 = vtk.vtkDICOMImageReader()
# v16.SetDirectoryName('D:/dicom_image/V')
v16.SetDirectoryName('D:/dicom_image/vtkDicomRender-master/sample')

# 利用封装好的MC算法抽取等值面，对应filter
marchingCubes = vtk.vtkMarchingCubes()
marchingCubes.SetInputConnection(v16.GetOutputPort())
marchingCubes.SetValue(0, -10)

# 剔除旧的或废除的数据单元，提高绘制速度，对应filter
Stripper = vtk.vtkStripper()
Stripper.SetInputConnection(marchingCubes.GetOutputPort())

# 建立映射，对应mapper
mapper = vtk.vtkPolyDataMapper()
# mapper.SetInputConnection(marchingCubes.GetOutputPort())
mapper.SetInputConnection(Stripper.GetOutputPort())

# 建立角色以及属性的设置，对应actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
# 角色的颜色设置
actor.GetProperty().SetDiffuseColor(1, .94, .25)
# 设置高光照明系数
actor.GetProperty().SetSpecular(.1)
# 设置高光能量
actor.GetProperty().SetSpecularPower(100)

# 定义舞台，也就是渲染器，对应render
renderer = vtk.vtkRenderer()

# 定义舞台上的相机，对应render
aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(0, 1, 0)
aCamera.SetFocalPoint(0, 0, 0)
aCamera.ComputeViewPlaneNormal()

# 定义整个剧院(应用窗口)，对应renderwindow
rewin = vtk.vtkRenderWindow()

# 定义与actor之间的交互，对应interactor
interactor = vtk.vtkRenderWindowInteractor()

# 将相机添加到舞台renderer
renderer.SetActiveCamera(aCamera)
aCamera.Dolly(1.5)

# 设置交互方式
style = vtk.vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(style)

# 将舞台添加到剧院中
rewin.AddRenderer(renderer)
interactor.SetRenderWindow(rewin)

# 将角色添加到舞台中
renderer.AddActor(actor)

# 将相机的焦点移动至中央，The camera will reposition itself to view the center point of the actors,
# and move along its initial view plane normal
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()





