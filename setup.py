from cx_Freeze import setup, Executable

files = ["img/matraz.ico"]

target = Executable(
    script="CotizaLab.pyw",
    base="Win32GUI",
    icon="img/matraz.ico"
)

setup(
    name="CotizaLab",
    version="1.0",
    description="CotizaLab",
    author="KumonDev",
    options={"build.exe" : {"include_files": files}},
    executables=[target]
)