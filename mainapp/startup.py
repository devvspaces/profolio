"""Startup script to setup project for usage
"""

import os
import secrets


def create_log_dir():
    """Create log directory if it doesn't exist
    """
    log_dir = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)


def create_random_secret_key():
    """Create a random secret key
    """
    length = 50
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for i in range(length))


def create_env_file():
    """Create .env file if it doesn't exist
    """
    env_file = os.path.join(os.getcwd(), '.env')
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:

            # Create a random secret key
            secret_key = create_random_secret_key()

            f.write(f'DJANGO_SECRET_KEY={secret_key}')
            f.write('DEBUG=True')


def main():
    """Main function
    """
    create_log_dir()
    create_env_file()


if __name__ == '__main__':
    main()
