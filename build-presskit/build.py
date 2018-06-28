#!/usr/bin/env python3
from glob import glob
from shutil import copy
from os import remove, path
from subprocess import check_output
import os

def main():
    screenshots = glob("../images/screenshots/highres/*.png")
    additional_files = glob("../press/images/*.*")
    print("Copying files")
    for f in screenshots + additional_files:
        copy(f, "images/")

    print("Generating index")
    with open(os.devnull, "w") as fnull:
        output = check_output(["/usr/bin/env", "php", "index.php"], stderr=fnull)

    output = output.decode("utf-8")

    for screenshot in screenshots:
        fn = path.join("images",path.basename(screenshot))
        output = output.replace(fn, screenshot)

    output = output.replace("sheet.php?p=credits", "credits.html")

    with open("../press/index.html", "w") as f:
        f.write(output)

    copy("style.css", "../press/")

    with open(os.devnull, "w") as fnull:
        credits_output = check_output(["/usr/bin/env", "php", "-r", "$_GET['p']='credits';include('sheet.php');"]).decode("utf-8")

    credits_output = credits_output.replace("credits.php", "credits-content.html")
    
    with open(os.devnull, "w") as fnull:
        credits_content = check_output(["/usr/bin/env", "php", "credits.php"]).decode("utf-8")
    
    with open("../press/credits.html", "w") as f:
        f.write(credits_output)

    with open("../press/credits-content.html", "w") as f:
        f.write(credits_content)
   

    print("Deleting files")
    for f in screenshots + additional_files:
        f = path.join("images",path.basename(f))
        remove(f)


if __name__ == "__main__":
    main()
