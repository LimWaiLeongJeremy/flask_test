from sqlalchemy import text

# DROP TABLE QUERIES
DRP_TSK_TBL_QRY = text("""
    DROP TABLE IF EXISTS tasks;                    
""")
DRP_USR_TBL_QRY = text("""
    DROP TABLE IF EXISTS users;                    
""")
DRP_TSK_PRO_TBL_QRY = text("""
    DROP TABLE IF EXISTS task_process;                    
""")
DRP_RLE_TBL_QRY = text("""
    DROP TABLE IF EXISTS roles;                    
""")
DRP_USR_HAS_RLE_TBL_QRY = text("""
    DROP TABLE IF EXISTS user_has_roles;                    
""")
DRP_PERM_TBL_QRY = text("""
    DROP TABLE IF EXISTS permissions;                    
""")
DRP_RLE_HAS_PERM_TBL_QRY = text("""
    DROP TABLE IF EXISTS roles_has_permissions;                    
""")


# CREATE TABLE QUERIES
CRT_TSK_TBL_QRY = text("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        points INT NOT NULL,
        image_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
""")

CRT_USR_TBL_QRY = text("""
    CREATE TABLE IF NOT EXISTS users (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL, 
        email VARCHAR(120) UNIQUE NOT NULL
    ) ENGINE=InnoDB;
""")

CRT_TSK_PRO_TBL_QRY = text("""
    CREATE TABLE IF NOT EXISTS task_process (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        task_id INT NOT NULL,
        user_id INT NOT NULL,
        notes TEXT,
        completed_at TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES tasks(id)
            ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE
    ) ENGINE=InnoDB;
""")

CRT_RLE_TBL_QRY = text("""
    CREATE TABLE IF NOT EXISTS roles (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        role VARCHAR(50) UNIQUE NOT NULL 
    ) ENGINE=InnoDB;
""")

CRT_PERM_TBL_QRY = text("""
    CREATE TABLE IF NOT EXISTS permissions (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        permission VARCHAR(100) UNIQUE NOT NULL 
    ) ENGINE=InnoDB;
""")
CRT_USR_HAS_RLE_TBL_QRY = text("""
    CREATE TABLE IF NOT EXISTS user_has_roles (
        user_id INT NOT NULL,
        role_id INT NOT NULL,
        PRIMARY KEY (user_id, role_id),
        FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES roles(id)
            ON DELETE CASCADE
    ) ENGINE=InnoDB;
""")
CRT_RLE_HAS_PERM_TBL_QRY = text("""
    CREATE TABLE IF NOT EXISTS roles_has_permissions (
        role_id INT NOT NULL,
        permission_id INT NOT NULL,
        PRIMARY KEY (role_id, permission_id),
        FOREIGN KEY (role_id) REFERENCES roles(id)
            ON DELETE CASCADE,
        FOREIGN KEY (permission_id) REFERENCES permissions(id)
            ON DELETE CASCADE
    ) ENGINE=InnoDB;
""")

# UPDATE QUERIES
UPD_TSK_QRY = text("""
    UPDATE tasks
    SET     
        name = :name, 
        description = :description, 
        points = :points, 
        image_url = :image_url
    WHERE 
        tasks.id = :task_id;                   
""")


# INSERT QUERIES
INS_RLE_QRY = text("""
    INSERT INTO roles (role) VALUES (:role);
""")

INS_USR_RLE_QRY = text("""
    INSERT INTO user_has_roles (user_id, role_id) 
    VALUES (:user_id, :role_id);
""")

INS_PERM_QRY = text("""
    INSERT INTO permissions (permission) VALUES (:permission);
""")

INS_RLE_PERM_QRY = text("""
    INSERT INTO roles_has_permissions (role_id, permission_id) 
    VALUES (:role_id, :permission_id);
""")

INS_USR_QRY = text("""
    INSERT INTO users (username, password, email)
    VALUES (:username, :password, :email);
""")

INS_TSK_QRY = text("""
    INSERT INTO tasks (name, description, points, image_url)    
    VALUES (:name, :description, :points, :image_url);
""")


# SELECT QUERIES
SEL_ALL_RLE_QRY = text("""
    SELECT * FROM roles;
""")

SEL_PERM_QRY = text("""
    SELECT * FROM permissions;
""")

SEL_TSK_BY_ID = text("""
    SELECT 
        name,
        description,
        points, 
        image_url
    FROM 
        tasks
    WHERE 
        id = :task_id                 
""")

SEL_USR_BY_USR_NAME = text("""
    SELECT 
        * 
    FROM 
        users 
    WHERE 
        username = :username;                    
""")


# get last insert id
LST_IST_QRY = text('SELECT LAST_INSERT_ID();')
LST_IST_QRY_FRM_RLE = text('SELECT LAST_INSERT_ID() FROM roles;')
LST_IST_QRY_FRM_PERM = text('SELECT LAST_INSERT_ID() FROM permissions;')
