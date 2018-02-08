########################################
# Fabfile to:
#    - deploy supporting HA components
#    - deploy HA
########################################

# Import Fabric's API module
from fabric.api import *
import fabric.contrib.files
import time
import os


env.hosts = ['localhost']
env.user = "pi"
env.password = "raspberry"
env.warn_only = True
pi_hardware = os.uname()[4]

#######################
## Core server setup ##
#######################

def install_start():
    """ Notify of install start """
    print("""
    ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,,,, ,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,,,   ,,,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,,     ,,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,       ,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,         ,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,           ,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,             ,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,               ,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,       ,,,,,     ,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,       ,,,,,,,     ,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,       ,,,,,,,,,     ,,,     ,,,,,,,,,,
    ,,,,,,,,,,,,,,,,        ,,,   ,,,      ,,     ,,,,,,,,,,
    ,,,,,,,,,,,,,,,         ,,,   ,,,       ,     ,,,,,,,,,,
    ,,,,,,,,,,,,,,          ,,,   ,,,             ,,,,,,,,,,
    ,,,,,,,,,,,,,            ,,,,,,,              ,,,,,,,,,,
    ,,,,,,,,,,,,              ,,,,,               ,,,,,,,,,,
    ,,,,,,,,,,,                ,,,                ,,,,,,,,,,
    ,,,,,,,,,,                 ,,,                 ,,,,,,,,,
    ,,,,,,,,,        ,,,       ,,,       ,,,        ,,,,,,,,
    ,,,,,,,,       ,,,,,,,     ,,,     ,,,,,,,       ,,,,,,,
    ,,,,,,,       ,,,,,,,,,    ,,,    ,,,,,,,,,       ,,,,,,
    ,,,,,,        ,,,   ,,,    ,,,    ,,,   ,,,        ,,,,,
    ,,,,,         ,,,   ,,,    ,,,    ,,,   ,,,         ,,,,
    ,,,,,,,,,,,   ,,,   ,,,    ,,,    ,,,   ,,,   ,,,,,,,,,,
    ,,,,,,,,,,,    ,,,,,,,,    ,,,    ,,,,,,,,    ,,,,,,,,,,
    ,,,,,,,,,,,      ,,,,,,    ,,,    ,,,,,,      ,,,,,,,,,,
    ,,,,,,,,,,,        ,,,,,   ,,,   ,,,,,        ,,,,,,,,,,
    ,,,,,,,,,,,          ,,,, ,,,, ,,,,,          ,,,,,,,,,,
    ,,,,,,,,,,,           ,,,, ,,, ,,,,           ,,,,,,,,,,
    ,,,,,,,,,,,            ,,,,,,,,,,,            ,,,,,,,,,,
    ,,,,,,,,,,,             ,,,,,,,,,             ,,,,,,,,,,
    ,,,,,,,,,,,              ,,,,,,,              ,,,,,,,,,,
    ,,,,,,,,,,,               ,,,,,               ,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,                                   ,,,,,,,,,,
    ,,,,,,,,,,,   Welcome to the Home Assistant   ,,,,,,,,,,
    ,,,,,,,,,,, Raspberry Pi All-In-One Installer ,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    """)
    print("* Warning *")
    print("""此脚本仅限初次安装 Home Assistant 使用""")
    time.sleep(10)
    print("启动安装器...")
    print("安装完成后，你的树莓派将重启。")
    time.sleep(5)



def update_upgrade():
    """ Update OS """
    sudo("apt-get update")
    sudo("apt-get upgrade -y")


def setup_dirs():
    """ Create all needed directories and change ownership """
    with cd("/srv"):
        sudo("mkdir homeassistant")
        sudo("chown homeassistant:homeassistant homeassistant")
        with cd("homeassistant"):
            sudo("mkdir -p src")
            sudo("chown homeassistant:homeassistant src")
    with cd("/home"):
        sudo("mkdir -p homeassistant")
        sudo("mkdir -p /home/homeassistant/.homeassistant")
        sudo("chown homeassistant:homeassistant homeassistant")
    with cd("/var/lib/"):
        sudo("mkdir mosquitto")
        sudo("chown mosquitto:mosquitto mosquitto")


def new_user(admin_username, admin_password):
    env.user = 'root'

    # Create the admin group and add it to the sudoers file
    admin_group = 'admin'
    runcmd('addgroup {group}'.format(group=admin_group))
    runcmd('echo "%{group} ALL=(ALL) ALL" >> /etc/sudoers'.format(
        group=admin_group))

    # Create the new admin user (default group=username); add to admin group
    runcmd('adduser {username} --disabled-password --gecos ""'.format(
        username=pi))
    runcmd('adduser {username} {group}'.format(
        username=admin_username,
        group=admin_group))

    # Set the password for the new admin user
    runcmd('echo "{username}:{password}" | chpasswd'.format(
        username=admin_username,
        password=admin_password))


def setup_users():
    """ Create service users, etc """
    sudo("useradd mosquitto")
    sudo("useradd --system homeassistant")
    sudo("usermod -G dialout -a homeassistant")
    sudo("usermod -G gpio -a homeassistant")
    sudo("usermod -G video -a homeassistant")
    sudo("usermod -d /home/homeassistant homeassistant")

def install_syscore():
    """ Download and install Host Dependencies. """
    sudo("aptitude install -y build-essential")
    sudo("aptitude install -y python-pip")
    sudo("aptitude install -y python-dev")
    sudo("aptitude install -y python3")
    sudo("aptitude install -y python3-dev")
    sudo("aptitude install -y python3-pip")
    sudo("aptitude install -y python3-sphinx")
    sudo("aptitude install -y python3-setuptools")
    sudo("aptitude install -y git")
    sudo("aptitude install -y libssl-dev")
    sudo("aptitude install -y cmake")
    sudo("aptitude install -y libc-ares-dev")
    sudo("aptitude install -y uuid-dev")
    sudo("aptitude install -y daemon")
    sudo("aptitude install -y curl")
    sudo("aptitude install -y libgnutls28-dev")
    sudo("aptitude install -y libgnutlsxx28")
    sudo("aptitude install -y libgnutls-dev")
    sudo("aptitude install -y nmap")
    sudo("aptitude install -y net-tools")
    sudo("aptitude install -y sudo")
    sudo("aptitude install -y libglib2.0-dev")
    sudo("aptitude install -y cython3")
    sudo("aptitude install -y libudev-dev")
    sudo("aptitude install -y libxrandr-dev")
    sudo("aptitude install -y swig")

def install_pycore():
    """ Download and install VirtualEnv """
    sudo("pip3 install --upgrade pip")
    sudo("pip3 install virtualenv")

def create_venv():
    """ Create home-assistant VirtualEnv """
    with cd("/srv/homeassistant"):
            sudo("virtualenv -p python3 homeassistant_venv", user="homeassistant")


#######################################################
## Build and Install Applications without VirtualEnv ##
#######################################################

def setup_homeassistant_novenv():
    """ Install Home-Assistant """
    sudo("pip3 install --upgrade pip", user="homeassistant")
    sudo("pip3 install homeassistant", user="homeassistant")

def setup_services_novenv():
    """ Enable applications to start at boot via systemd """
    hacfg="""
mqtt:
  broker: 127.0.0.1
  port: 1883
  client_id: home-assistant-1
  username: pi
  password: raspberry
"""
    with cd("/etc/systemd/system/"):
        put("home-assistant_novenv.service", "home-assistant_novenv.service", use_sudo=True)
    with settings(sudo_user='homeassistant'):
        sudo("/srv/homeassistant/homeassistant_venv/bin/hass --script ensure_config --config /home/homeassistant/.homeassistant")

    fabric.contrib.files.append("/home/homeassistant/.homeassistant/configuration.yaml", hacfg, use_sudo=True)
    sudo("systemctl enable home-assistant_novenv.service")
    sudo("systemctl daemon-reload")

####################################
## Build and Install Applications ##
####################################

def setup_mosquitto():
    """ Install Mosquitto w/ websockets"""
    with cd("/srv/homeassistant/src"):
        sudo("curl -O http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key")
        sudo("apt-key add mosquitto-repo.gpg.key")
        with cd("/etc/apt/sources.list.d/"):
            sudo("curl -O http://repo.mosquitto.org/debian/mosquitto-stretch.list")
            sudo("apt-get update")
            sudo("apt-cache search mosquitto")
            sudo("apt-get install -y mosquitto mosquitto-clients")
            with cd("/etc/mosquitto"):
                put("mosquitto.conf", "mosquitto.conf", use_sudo=True)
                sudo("touch pwfile")
                sudo("chown mosquitto: pwfile")
                sudo("chmod 0600 pwfile")
                sudo("sudo mosquitto_passwd -b pwfile pi raspberry")
                sudo("sudo chown mosquitto: mosquitto.conf")

def setup_homeassistant():
    """ Activate Virtualenv, Install Home-Assistant """
    sudo("source /srv/homeassistant/homeassistant_venv/bin/activate && pip3 install homeassistant", user="homeassistant")
    with cd("/home/homeassistant/"):
        sudo("chown -R homeassistant:homeassistant /home/homeassistant/")

def setup_services():
    """ Enable applications to start at boot via systemd """
    with cd("/etc/systemd/system/"):
        put("home-assistant.service", "home-assistant.service", use_sudo=True)
    with settings(sudo_user='homeassistant'):
        sudo("/srv/homeassistant/homeassistant_venv/bin/hass --script ensure_config --config /home/homeassistant/.homeassistant")


    hacfg="""
mqtt:
  broker: 127.0.0.1
  port: 1883
  client_id: home-assistant-1
  username: pi
  password: raspberry
"""


    fabric.contrib.files.append("/home/homeassistant/.homeassistant/configuration.yaml", hacfg, use_sudo=True)
    sudo("systemctl enable home-assistant.service")
    sudo("systemctl daemon-reload")
    sudo("systemctl start home-assistant.service")
    
def upgrade_homeassistant():
    """ Activate Venv, and upgrade Home Assistant to latest version """
    sudo("source /srv/homeassistant/homeassistant_venv/bin/activate && pip3 install homeassistant --upgrade", user="homeassistant")

#############
## Deploy! ##
#############

def deploy():

    ## Install Start ##
    install_start()

    ## Initial Update and Upgrade ##
    update_upgrade()

    ## Setup service accounts ##
    setup_users()

    ## Setup directories ##
    setup_dirs()

    ## Install dependencies ##
    install_syscore()
    install_pycore()

    ## Create VirtualEnv ##
    create_venv()

    ## Build and Install Mosquitto ##
    setup_mosquitto()

    ## Activate venv, install Home-Assistant ##
    setup_homeassistant()

    ## Make apps start at boot ##
    setup_services()

    ## Reboot the system ##
    reboot()




def deploy_novenv():

    ## Install Start ##
    install_start()

    ## Initial Update and Upgrade ##
    update_upgrade()

    ## Setup service accounts ##
    setup_users()

    ## Setup directories ##
    setup_dirs()

    ## Install dependencies ##
    install_syscore()

    ## Build and Install Mosquitto ##
    setup_mosquitto()

    ## Activate venv, install Home-Assistant ##
    setup_homeassistant_novenv()

    ## Make apps start at boot ##
    setup_services_novenv()

    ## Reboot the system ##
    reboot()
