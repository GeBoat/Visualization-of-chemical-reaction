from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from werkzeug.utils import secure_filename
import os
import logging
from function.environment.flask.file import organize_files
from function.environment.python_getData.newOS import main
from function.environment.python_getData.mysql import datebaseCheck
app = Flask(__name__)
app.secret_key = 'abcd'

# 获取当前脚本所在的目录作为基准
base_dir = os.path.dirname(os.path.abspath(__file__))
# 计算目标上传文件夹的绝对路径
upload_folder_path = os.path.join(base_dir, '..\..\..', 'reference', 'ben id')
filepath = os.path.join(base_dir, '..\..\..', 'reference')
# 设置 Flask 配置中的 UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = upload_folder_path
# 确保该路径存在，如果不存在则创建
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
# 在设置 UPLOAD_FOLDER 后打印路径
log.info(f"Upload folder path: {app.config['UPLOAD_FOLDER']}")

@app.route('/mysql', methods=['GET', 'POST'])
def mysql():
    error_message = None  # 初始化错误消息为空

    if request.method == 'POST':
        user = request.form.get('db_account')
        password = request.form.get('db_password')
        port = request.form.get('db_port')
        if not all(user or password or port):
            error_message = '不能有空值'
        port = int(port)

        connection_status = datebaseCheck(user, password, port)

        if connection_status == "success":
            # 连接成功，可以进一步执行数据库操作
            sqllist = {'user': user, 'password': password, 'port': port}
            session['sqllist'] = sqllist
            response = make_response(jsonify({"data": {"success": True}}))
            # print(session['sqllist'])
            # db_link = mysqlLink(user, password)
        else:
            # 连接失败，设置错误信息
            error_message = '账号密码不正确.'
            response = make_response(jsonify({"data": {"错误：": error_message}}), 400)

        return response

@app.route('/open_file', methods=['GET', 'POST'])
def open_file():
    error_message = None
    success = False
    print("11111111111111")
    if request.method == 'POST':
        # 检查 files 是否在 request.files 中
        if 'files' not in request.files:
            error_message = "上传失败，请重新上传"
        else:
            files = request.files.getlist('files')
            print(files)
            # 逐个处理上传的文件
            for file in files:
                filename = secure_filename(file.filename)
                try:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    success = True
                except Exception as e:
                    error_message = f"上传过程中发生错误: {str(e)}"
                    print(error_message)

            if success:
                organize_files(app.config['UPLOAD_FOLDER'])

    # 如果上传成功，则返回 200 OK 响应
    if success:
        response = make_response(jsonify({"status": "success"}))
        response.status_code = 200
        print(response.status_code)
    else:
        # 如果有错误信息，则渲染模板并传递参数
        response = render_template('index.html', current_page="open_file", error_message=error_message)

    return response

@app.route("/chart", methods=['GET', 'POST'])
def chart():
    if request.method == 'POST':
        # 接收前端传来的图表类型列表（以逗号分隔）
        json_data = request.get_json()
        chartlist = json_data.get('selectedIds', [])  # 获取 selectedIds 字段，若不存在则返回空列表
        print("chartlist", chartlist)
        session['chartlist'] = chartlist

        main(session['sqllist'], filepath, session['chartlist'])
        response = make_response(jsonify({"status": "success"}))
        response.status_code = 200
        return response

    return render_template('chart.html', current_page="chart")


@app.route('/over', methods=['GET'])
def over():
    chart_list = session.get('chartlist', [])
    return render_template('over.html', chart_list=chart_list,current_page="over")

@app.route('/')
def home():
    return render_template('index.html', current_page='index')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
