from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from combine_photos import create_photo_doc, create_preview
import tempfile
import shutil

app = Flask(__name__)

# 配置临时文件夹
TEMP_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = TEMP_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/preview', methods=['POST'])
def preview_doc():
    work_dir = None
    try:
        # 获取上传的文件和标题
        title = request.form['title']
        photo1 = request.files['photo1']
        photo2 = request.files['photo2']

        # 创建临时工作目录
        work_dir = tempfile.mkdtemp()
        
        # 保存上传的图片
        img1_path = os.path.join(work_dir, '1.jpg')
        img2_path = os.path.join(work_dir, '2.jpg')
        photo1.save(img1_path)
        photo2.save(img2_path)

        # 生成预览
        preview_base64 = create_preview(title, img1_path, img2_path)
        
        return jsonify({'preview': preview_base64})

    except Exception as e:
        print(f"Error in preview_doc: {str(e)}")
        return str(e), 500

    finally:
        # 清理临时文件
        try:
            if work_dir and os.path.exists(work_dir):
                shutil.rmtree(work_dir)
        except Exception as e:
            print(f"Error cleaning up: {str(e)}")

@app.route('/api/combine-photos', methods=['POST'])
def combine_photos():
    work_dir = None
    try:
        # 获取上传的文件和标题
        title = request.form['title']
        photo1 = request.files['photo1']
        photo2 = request.files['photo2']

        # 创建临时工作目录
        work_dir = tempfile.mkdtemp()
        
        # 保存上传的图片
        img1_path = os.path.join(work_dir, '1.jpg')
        img2_path = os.path.join(work_dir, '2.jpg')
        photo1.save(img1_path)
        photo2.save(img2_path)

        print(f"Title: {title}")
        print(f"Working directory: {work_dir}")
        print(f"Saved images to: {img1_path}, {img2_path}")

        # 检查文件是否存在和大小
        if not os.path.exists(img1_path) or not os.path.exists(img2_path):
            raise Exception("图片保存失败")
        
        if os.path.getsize(img1_path) == 0 or os.path.getsize(img2_path) == 0:
            raise Exception("上传的图片文件为空")

        # 生成文档
        output_filename = f'照片丨{title}.docx'
        doc_path = os.path.join(work_dir, output_filename)
        
        try:
            # 生成文档
            create_photo_doc(title, img1_path, img2_path, doc_path)
            
            # 检查文档是否生成
            if not os.path.exists(doc_path):
                raise Exception("文档生成失败")
                
            # 发送文件
            return send_file(
                doc_path,
                as_attachment=True,
                download_name=output_filename,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )

        except Exception as e:
            print(f"Error in document creation: {str(e)}")
            raise Exception(f"文档生成失败: {str(e)}")

    except Exception as e:
        print(f"Error in combine_photos: {str(e)}")
        return str(e), 500

    finally:
        # 清理临时文件
        try:
            if work_dir and os.path.exists(work_dir):
                shutil.rmtree(work_dir)
        except Exception as e:
            print(f"Error cleaning up: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True) 