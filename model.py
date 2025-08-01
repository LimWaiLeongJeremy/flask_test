from extension import db
from sqlalchemy.exc import SQLAlchemyError
import repo
import bcrypt
import os


# Initialize the database by dropping existing tables, creating new ones, and populating roles and permissions.
def drop_tables():
    try:
        with db.engine.begin() as conn:
            # Drop existing tables
            conn.execute(repo.DRP_RLE_HAS_PERM_TBL_QRY)
            conn.execute(repo.DRP_PERM_TBL_QRY)
            conn.execute(repo.DRP_USR_HAS_RLE_TBL_QRY)
            conn.execute(repo.DRP_RLE_TBL_QRY)
            conn.execute(repo.DRP_TSK_PRO_TBL_QRY)
            conn.execute(repo.DRP_USR_TBL_QRY)
            conn.execute(repo.DRP_TSK_TBL_QRY)

            # Commit the changes
            conn.commit()

    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error deleting tables: {e}")
        raise e


def create_tables():
    try:
        with db.engine.begin() as conn:
            # Create new tables
            conn.execute(repo.CRT_TSK_TBL_QRY)
            conn.execute(repo.CRT_USR_TBL_QRY)
            conn.execute(repo.CRT_TSK_PRO_TBL_QRY)
            conn.execute(repo.CRT_RLE_TBL_QRY)
            conn.execute(repo.CRT_USR_HAS_RLE_TBL_QRY)
            conn.execute(repo.CRT_PERM_TBL_QRY)
            conn.execute(repo.CRT_RLE_HAS_PERM_TBL_QRY)

            # Commit the changes
            conn.commit()
            return True

    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error creating tables: {e}")
        raise e


def init_roles():
    try:
        with db.engine.begin() as conn:
            # Check if roles exist
            roles_id = conn.execute(repo.LST_IST_QRY_FRM_RLE).fetchone()

            # If roles are not populated, insert default roles
            if roles_id == None:
                print("Role not populated")

                # Insert default roles
                conn.execute(repo.INS_RLE_QRY, {'role': 'admin'})
                conn.execute(repo.INS_RLE_QRY, {'role': 'user'})

                # Commit the changes
                conn.commit()
            return True

    except SQLAlchemyError as e:
        print(f"Error inserting roles: {e}")
        raise e


def init_permissions():
    try:
        with db.engine.begin() as conn:
            # Check if roles exist
            roles = conn.execute(repo.LST_IST_QRY_FRM_PERM).fetchone()

            # If roles are not populated, insert default roles
            if roles == None:
                print("Permissions not populated")

                # Insert default permissions
                conn.execute(repo.INS_PERM_QRY, {'permission': 'create_task'})
                conn.execute(repo.INS_PERM_QRY, {'permission': 'view_task'})
                conn.execute(repo.INS_PERM_QRY, {'permission': 'update_task'})
                conn.execute(repo.INS_PERM_QRY, {'permission': 'delete_task'})
                conn.execute(repo.INS_PERM_QRY, {'permission': 'administer_users'})

                # Assign permissions to roles
                conn.execute(repo.INS_RLE_PERM_QRY, {
                             'role_id': 1, 'permission_id': 5})  # Admin role
                conn.execute(repo.INS_RLE_PERM_QRY, {
                             'role_id': 2, 'permission_id': 1})  # User create role
                conn.execute(repo.INS_RLE_PERM_QRY, {
                             'role_id': 2, 'permission_id': 2})  # User view role
                conn.execute(repo.INS_RLE_PERM_QRY, {
                             'role_id': 2, 'permission_id': 3})  # User update role
                conn.execute(repo.INS_RLE_PERM_QRY, {
                             'role_id': 2, 'permission_id': 4})  # User delete role

            # Commit the changes
            conn.commit()
            return True

    except SQLAlchemyError as e:
        print(f"Error inserting permissions: {e}")
        raise e


def create_admin_user():
    if create_user('admin', 'admin', 'admin@mail.com'):
        return True


def init_db():
    if drop_tables():
        print("Tables deleted successfully.")
    if create_tables():
        print("Tables created successfully.")
    if init_roles():
        print("Roles initialized successfully.")
    if init_permissions():
        print("Permissions initialized successfully.")
    if create_admin_user():
        print("Admin user created successfully.")


# ========== Task Management Functions ==========
def create_task(name, description, points, image_url):
    try:
        with db.engine.begin() as conn:
            # Insert the task into the database
            conn.execute(repo.INS_TSK_QRY, {
                'name': name,
                'description': description,
                'points': points,
                'image_url': image_url
            })
            # Get the last inserted task ID
            task_id = conn.execute(repo.LST_IST_QRY).fetchone()[0]

            # Commit the changes
            conn.commit()
            return task_id

    except SQLAlchemyError as e:
        print(f"Error creating task: {e}")
        raise e


def create_user(username, password, email):
    # Encrypt the password
    # Using bcrypt to hash the password
    # and adding a salt for security and if more than one user have the same password the encrypted password will be different
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    if not get_user_by_username(username):
        try:
            with db.engine.begin() as conn:
                # Insert admin user
                conn.execute(repo.INS_USR_QRY, {
                    'username': username,
                    'password': password,
                    'email': email
                })
                # Get the last inserted user ID
                user_id = conn.execute(repo.LST_IST_QRY).fetchone()[0]
                # Assign the admin role to the user
                if username == 'admin':
                    conn.execute(repo.INS_USR_RLE_QRY, {
                        'user_id': user_id,
                        'role_id': 1  # Admin role ID
                    })
                else:
                    conn.execute(repo.INS_USR_RLE_QRY, {
                        'user_id': user_id,
                        'role_id': 2  # User role ID
                    })

                return user_id
        except SQLAlchemyError as e:
            print(f"Error creating user: {e}")
            raise e
    else:
        print("User already created.")


def update_task(task_id, name, description, points, image_url):
    try:
        with db.engine.begin() as conn:
            # Update the task
            conn.execute(repo.UPD_TSK_QRY, {
                'task_id': task_id,
                'name': name,
                'description': description,
                'points': points,
                'image_url': image_url
            })

            # Commit the changes
            conn.commit()
            return True

    except SQLAlchemyError as e:
        print(f"Error updating task: {e}")
        raise e


def get_task_by_id(task_id):
    try:
        with db.engine.begin() as conn:
            task = conn.execute(repo.SEL_TSK_BY_ID, {
                                'task_id': task_id}).fetchone()
            return task
    except Exception as e:
        print('Error getting task')
        raise e


def get_user_by_username(username):
    try:
        with db.engine.begin() as conn:
            user = conn.execute(repo.SEL_USR_BY_USR_NAME, {
                                'username': username}).fetchone()
            print(f"User: {user}")
            return user
    except Exception as e:
        print('Error getting user')
        raise e

# Function to velidate image file type


def allowed_file(filename):
    allowed_type = {'png', 'jpg', 'jpeg'}
    if '.' not in filename:
        return False
    # Split the filename to get extension
    ext = filename.rsplit('.', 1)[1].lower()
    # Check if file extension is in the list above

    if ext in allowed_type:
        return True
    return False

# Saving image
# setting user_id as 0 for testing


def save_image(image, user_id=0):
    base_path = 'static/uploads/image'  # Setting base path for image storage

    # Validate image
    if not image or image.filename == "":
        return "No image uploaded"
    # Validate image type
    if not allowed_file(image.filename):
        return "File type not allowed"

    user_dir = os.path.join(base_path, f'user_{user_id}/')  # Setting save path
    os.makedirs(user_dir, exist_ok=True)    # creating image directory

    # write image into application
    image_path = os.path.join(user_dir, image.filename)
    image.save(image_path)

    return image_path
