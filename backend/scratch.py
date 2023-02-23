import os
import pathlib as path


root = path.Path.cwd().parent
png_path = root.as_posix() + "frontend/dashboard/imgs"


print(png_path)