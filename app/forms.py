from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from flask_wtf.file import FileAllowed
from app.models.user import User, Role, user_roles
from app.models.tutorial import Category, Tag, Tutorial, tutorial_tags
from app.models.community import DiscussionPost, PostComment, PostLike
from app.models.resource import ResourceCategory, Resource, Download



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        from app.models.user import User
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        from app.models.user import User
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password (leave blank to keep unchanged)')
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Save')

class RoleForm(FlaskForm):
    name = StringField('Role Name', validators=[DataRequired(), Length(max=64)])
    description = StringField('Description', validators=[Length(max=200)])
    submit = SubmitField('Save')


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Description')
    sort_order = IntegerField('Sort Order', default=0)
    submit = SubmitField('Save')

class TagForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Save')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    bio = TextAreaField('About me', validators=[Length(max=500)])
    
    # ==================== Avatar Upload (只限 JPG / PNG) ====================
    avatar = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPG and PNG files are allowed!')
    ])
    # =====================================================================
    
    submit = SubmitField('Save Changes')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            from app.models.user import User
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken.')

    def validate_email(self, email):
        if email.data != self.original_email:
            from app.models.user import User
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered.')
        

class TutorialForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=200)])
    summary = TextAreaField('Summary')
    content = TextAreaField('Content', validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=[('beginner','Beginner'),('intermediate','Intermediate'),('advanced','Advanced')])
    estimated_minutes = IntegerField('Estimated Minutes', default=10, validators=[Optional()])
    is_published = BooleanField('Published')
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    tags = StringField('Tags (comma separated)', validators=[Optional()])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.models.tutorial import Category
        self.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[('general','General Discussion'),('help','Help Request'),('showcase','Showcase')])
    is_pinned = BooleanField('Pin this post (Admin only)')
    submit = SubmitField('Publish')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')


class ResourceCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=64)])
    icon = StringField('Icon class (Font Awesome)', validators=[Length(max=50)])
    description = TextAreaField('Description')
    submit = SubmitField('Save')

class ResourceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    type = SelectField('Type', choices=[('ebook','E-book'),('video','Video'),('sample','Sample Code'),('tool','Tool')])
    
    # ==================== GCS File Upload ====================
    file = FileField('Upload File', validators=[
        FileAllowed(['pdf', 'zip', 'docx', 'pptx', 'png', 'jpg', 'jpeg', 'mp4'], 
                   'Only PDF, ZIP, Images, Videos etc. allowed!')
    ])
    # =========================================================
    
    file_path = StringField('File Path or URL', validators=[Length(max=500)])
    external_link = StringField('External Link', validators=[Length(max=500)])
    file_size = StringField('File Size', validators=[Length(max=50)])
    is_featured = BooleanField('Featured')
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.models.resource import ResourceCategory
        self.category_id.choices = [(c.id, c.name) for c in ResourceCategory.query.all()] + [(0, 'Uncategorized')]

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', 
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')