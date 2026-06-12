from flask import render_template, Blueprint, make_response, request, url_for, flash, redirect
from app.models.tutorial import Tutorial
from app.models.resource import Resource
from flask_login import login_required, current_user
from app.forms import EditProfileForm         
from app.extensions import db               

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    latest_tutorials = Tutorial.query.filter_by(is_published=True).order_by(Tutorial.created_at.desc()).limit(5).all()
    featured_resources = Resource.query.filter_by(is_featured=True).order_by(Resource.created_at.desc()).limit(5).all()
    return render_template('index.html.j2', latest_tutorials=latest_tutorials, featured_resources=featured_resources)

@bp.route('/user/<username>')
@login_required
def user_profile(username):
    from app.models.user import User
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html.j2', user=user)

@bp.route('/set-language/<lang>')
def set_language(lang):
    if lang not in ['en', 'zh', 'ja', 'ko']:
        flash('Invalid language', 'danger')
        return redirect(request.referrer or url_for('main.index'))
    
    resp = make_response(redirect(request.referrer or url_for('main.index')))
    resp.set_cookie('preferred_language', lang, max_age=30*24*3600) 
    flash(f'Language preference set to {lang}', 'success')
    return resp

@bp.route('/show-cookie')
def show_cookie():
    lang = request.cookies.get('preferred_language', 'not set')
    return f'Your preferred language is: {lang}'


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        
        # Handle avatar upload to GCS
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file.filename != '':
                try:
                    import os
                    bucket_name = os.environ.get('GCS_BUCKET_NAME')
                    if not bucket_name:
                        flash('GCS Bucket not configured', 'danger')
                    else:
                        from google.cloud import storage
                        storage_client = storage.Client()
                        bucket = storage_client.bucket(bucket_name)
                        
                        # 使用 username 作為檔案名
                        filename = f"avatars/{current_user.username}_{file.filename}"
                        blob = bucket.blob(filename)
                        blob.upload_from_string(file.read(), content_type=file.content_type)
                        
                        current_user.avatar = f"https://storage.googleapis.com/{bucket_name}/{filename}"
                        flash('Profile picture uploaded successfully!', 'success')
                except Exception as e:
                    flash(f'Avatar upload failed: {str(e)}', 'danger')
        
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('main.user_profile', username=current_user.username))
    
    # Populate form
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.bio.data = current_user.bio
    
    return render_template('edit_profile.html.j2', form=form)