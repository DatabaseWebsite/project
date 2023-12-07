from .user_management import login_user
from .user_management import signup_admin
from .email import send_mail
from .user_management import update_avatar
from .user_management import get_user_info
from .auth import refresh_token
from .user_management import logout_user
from .user_management import change_password
from .course_management import create_course
from .course_management import all_course_info
from .user_management import update_current_course
from .user_management import xlsx_create_users
from .user_management import user_list
from .homework_management import create_homework
from .homework_management import submit_homework
from .homework_management import submit_score
from .user_management import create_single_user
from .user_management import user_selected_course
from .user_management import delete_user
from .user_management import delete_users
from .user_management import update_user_info
from .user_management import search_users
from .material_management import upload_material
from .material_management import material_list
from .material_management import download_multiple_materials
from .homework_management import homework_list
from .course_management import all_participants


ITEM_PER_PAGE = 3
