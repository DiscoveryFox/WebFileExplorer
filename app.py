import os
import platform

from flask import Flask, render_template, request, send_file, url_for

app = Flask(__name__)

__starting_dir = os.path.abspath(os.path.dirname(__file__))


def check_for_error_on_dir_entry(dir_to_check: str):
    """
    Checks if there are any errors if you try to enter the demanded directory.
    :param dir_to_check: str
    :return: tuple[bool, str]
    """
    old_dir_path = os.getcwd()
    try:
        os.chdir(dir_to_check)
        os.chdir(old_dir_path)
        return False, ''
    except PermissionError:
        return True, 'PermissionError on directory entry'
    finally:
        os.chdir(old_dir_path)


def get_all_files():
    """
    Returns a list of all files in the current directory.
    """
    return_files = []

    files = [x for x in os.listdir() if os.path.isfile(x)]
    for file in files:
        if is_picture(file):
            return_files.append((file, 'picture'))
        else:
            return_files.append((file, 'file'))
    return return_files


def check_for_errors_on_read():
    """
    Checks if there are any errors in the current directory.
    :return: str
    """
    try:
        get_all_files()
        return False, 'No Error'
    except PermissionError:
        return True, 'PermissionError on read.'


def convert_to_safe(file_name: str) -> str:
    """
    Converts a file name to a safe file name which can be sent through an url.
    :param file_name: str
    :return: str
    """
    return file_name.replace('#', '%HASHTAG%').replace(' ', 'SPACEBAR')


def convert_from_safe(file_name: str) -> str:
    """
    Converts a file name from a safe file name to a normal file name.
    :param file_name: str
    :return: str
    """
    return file_name.replace('%HASHTAG%', '#').replace('SPACEBAR', ' ')


def get_all_folders():
    """
    Returns a list of all folders in the current directory.
    """
    return [x for x in os.listdir() if os.path.isdir(x)]


def get_directory_name():
    """
    Returns the name of the current directory.
    :return: str
    """
    if platform.system() == 'Windows':
        return os.getcwd().split('\\')[-1]
    else:
        os.getcwd().split('/')[-1]


def is_picture(file_name):
    """
    Returns True if the file is a picture.
    :param file_name: str
    :return: bool
    """
    return file_name.split('.')[-1].lower() in ['jpg', 'jpeg', 'png', 'gif']


@app.context_processor
def inject_variables():
    """
    Injects variables into the templates.
    """
    return dict(
        len=len
    )


@app.route('/')
def index():
    return render_template('index.html', files=get_all_files(),
                           folders=get_all_folders(),
                           directoryname=get_directory_name(),
                           directorypath=os.getcwd(),
                           convert_from_safe=convert_from_safe,
                           convert_to_safe=convert_to_safe)


@app.route('/favicon.ico')
def favicon():
    os.chdir(__starting_dir)
    if platform.system() == 'Windows':
        return send_file('templates\\favicon.ico')
    else:
        return send_file('templates/favicon.ico')


@app.route('/<string:file_name>')
def show_file(file_name):
    file_name = convert_from_safe(file_name)
    # check if file_name is a directory or a file
    if os.path.isdir(file_name):
        old_dir = os.getcwd()

        if check_for_error_on_dir_entry(file_name)[0]:
            return render_template('error.html', error=check_for_error_on_dir_entry(file_name)[1])
        else:
            os.chdir(file_name)

        error = check_for_errors_on_read()
        if error[0]:
            os.chdir(old_dir)
            return render_template('error.html', error=error[1])
        else:
            pass


        return render_template('index.html', files=get_all_files(),
                               folders=get_all_folders(),
                               directoryname=get_directory_name(),
                               directorypath=os.getcwd(),
                               convert_from_safe=convert_from_safe,
                               convert_to_safe=convert_to_safe)
    else:
        if is_picture(file_name):
            return send_file(os.getcwd() + '/' + file_name,
                             mimetype='image/' + file_name.split('.')[-1])
        return render_template('file.html', file_name=file_name, file_content=open(file_name).read(
        ))


@app.route('/upper_directory')
def upper_directory():
    os.chdir('..')
    return render_template('index.html', files=get_all_files(),
                           folders=get_all_folders(),
                           directoryname=get_directory_name(),
                           directorypath=os.getcwd(),
                           convert_from_safe=convert_from_safe,
                           convert_to_safe=convert_to_safe)


@app.route('/save/<string:file_name>/', methods=["POST"])
def save_file(file_name):
    with open(file_name, 'w') as f:
        f.write(request.data.decode("utf-8"))
        return 'saved', 200


if __name__ == '__main__':
    app.run()
