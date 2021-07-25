import os
import sys
from time import sleep

from conf_wizard_net import conf_wizard_net
from conf_wizard_ota import conf_ota
from modules import clear_the_screen, Bcolors, logo_top, triangle_image_show, ota_asci_image_show, load_config, \
    load_ota_sys_markers, write_ota_sys_markers, get_ota_version
from rpi_update import main_window as rpi_update, rh_update_check
from nodes_flash import flashing_menu
from nodes_update_old import nodes_update as old_flash_gpio
from sensors_menu import sensors_menu as external_sensors_menu


def compatibility():  # adds compatibility and fixes with previous versions
    from prev_comp import main as prev_comp
    prev_comp()


def config_check():
    if not os.path.exists("./updater-config.json"):
        prompt = """
          {prompt}  Looks that you haven't set up config file yet.  {endc}
          {prompt}  Please enter configuration wizard - point 4     {endc}""" \
            .format(prompt=Bcolors.PROMPT, endc=Bcolors.ENDC)
        print(prompt)
        return False
    else:
        return True


def attribute_error_handling():
    err_msg = """
    AttributeError

    Looks that you may have some configuration mismatch. 
    Check entered username and other parameters in config wizard.

    You may also try to re-open the ota software with './ota.sh' command.

    """
    print(err_msg)
    input("\n\n\tHit Enter to continue and next check your configuration.")
    clear_the_screen()


def read_aliases_file():
    aliases_to_show = []
    with open('./resources/aliases.txt', 'r') as aliases_file:
        for line in aliases_file:
            if 'alias ' in line and '###' not in line:
                line = line.replace('alias ', '')
                line = line[0:line.index('=')] + ' ' + line[line.index('#'):-1]
                line = line.replace('#', '\t\t\t')
                aliases_to_show.append(line)
            elif '#' in line and '###' not in line:
                line = line.replace('#', '')
                aliases_to_show.append(line)
            elif '###' not in line:
                aliases_to_show.append(line)

    aliases_to_show = ('\n\t\t'.join(aliases_to_show))

    return aliases_to_show


def log_to_dev(config):
    log_write(config)
    log_send(config)


def log_write(config):
    os.system(f"./scripts/log_write.sh {config.user}")


def log_send(config):
    while True:
        selection = input("\n\n\tDo you want to send a log file for a review to the developer? [y/n] ")
        if selection == 'y' or selection == 'yes':
            log_name = input("\n\tPlease enter your name so we know who sent a log file: ")
            os.system(f"./scripts/log_send.sh {config.user} {log_name}")
            f = open("./log_data/log_code.txt", "r")
            code = ''
            for line in f:
                code = line
            code_error_msg = """
                -- Error occurred --

        Please send log file manually - from 'log_data' folder. 
        Uploading to server process has failed.
            """
            code_report = f"""
User code: {code}

------------------------------

"""
            print(code_report) if code != '' else print(code_error_msg)
        if selection == 'n' or selection == 'no':
            print("\n\nOK - your log file is stored as 'log.txt' in RH-ota/log_data/ directory.")
        input("\nHit 'Enter' to continue\n\n")
        if not os.system("cowsay You are awesome! Fly safe."):
            sleep(3)
        break


def updated_check(config):
    updated_recently_with_new_version_flag = os.path.exists(f"/home/{config.user}/.ota_markers/.was_updated_new")
    # true if self update was performed and new version was available to downloaded
    updated_recently_with_old_version_flag = os.path.exists(f"/home/{config.user}/.ota_markers/.was_updated_old")
    # true if self update was performed and version was not available to downloaded
    if updated_recently_with_new_version_flag:
        clear_the_screen()
        logo_top(config.debug_mode)
        print("""\n\n {bold}

            Software was updated recently to the new version.

            You can read update notes now.


             {endc}  {green} 
                r - Read update notes {endc}{yellow}

                s - Skip and don't show again{endc}
            """.format(bold=Bcolors.BOLD_S, endc=Bcolors.ENDC,
                       green=Bcolors.GREEN, yellow=Bcolors.YELLOW))
        while True:
            selection = input()
            if selection == 'r':
                os.system("less ./docs/update-notes.txt")
                sleep(0.5)
                break
            elif selection == 's':
                break
    os.system(f"rm /home/{config.user}/.ota_markers/.was_updated_new >/dev/null 2>&1")
    os.system(f"rm /home/{config.user}/.ota_markers/.was_updated_old >/dev/null 2>&1")
    if updated_recently_with_new_version_flag or updated_recently_with_old_version_flag:
        os.system("rm ./.first_time_here > /dev/null 2>&1")
        return True
    else:
        return False


def ota_update_available_check(config):
    # no config.user usage due to order of operations
    if os.path.exists("./.new_ota_version_diff_file") and os.path.exists("./updater-config.json"):
        if os.path.getsize("./.new_ota_version_diff_file"):
            ota_update_available_flag = True
        else:
            ota_update_available_flag = False  # done this way due to development purposes and weird edge cases
    else:
        ota_update_available_flag = False

    if ota_update_available_flag and config.beta_tester is False:  # don't show update prompt to beta-testers
        clear_the_screen()
        logo_top(config.debug_mode)
        print("""\n\n {bold}

                New OTA software release is available.
                
                Consider updating now (takes ~20 secs).



             {endc}  {green} 
                    u - Update now {endc}{yellow}

                    s - Skip{endc}
            """.format(bold=Bcolors.BOLD_S, endc=Bcolors.ENDC, red=Bcolors.RED,
                       green=Bcolors.GREEN, yellow=Bcolors.YELLOW))
        while True:
            selection = input()
            if selection == 'u':
                self_updater(config)
                break
            elif selection == 's':
                break


def welcome_screen(config):
    welcome_message = """{bold}
    Welcome to OTA! With our software you can easily install, update and manage 
    your RotorHazard installation. You can also flash the firmware onto nodes, 
    without the need to open the timer ever again. You have to use official PCB 
    or have 'hardware mod" done for that functionality. You may also check 
    features like smart-hotspot or adding aliases to your system, etc.


    This program has ability to perform 'self-updates' - see "Features Menu".    

    If you found any bug - please report it via GitHub or Facebook. {endc}{bold}        


    Wish you good experience. Enjoy!


                                                            Pawel F.                                                
    {endc}""".format(bold=Bcolors.BOLD, red=Bcolors.RED, green=Bcolors.GREEN, endc=Bcolors.ENDC)

    first_time_flag = os.path.exists("./.first_time_here")
    while first_time_flag and not updated_check(config):
        clear_the_screen()
        logo_top(config.debug_mode)
        print(welcome_message)
        selection = input(f"\n\t\t\t{Bcolors.GREEN}Open next page by typing 'n'{Bcolors.ENDC}\n\n").lower()
        if selection == 'n':
            os.system("rm ./.first_time_here")
            first_time_flag = False  # done that way so after configuration user won't be redirected back here
            show_about(config)
        if selection == 'f':  # helpful when troubleshooting, going further without changing the folder contents
            first_time_flag = False
            show_about(config)


"""
    After that you will be asked about system configuring.
    Please perform it, if you haven’t done it manually already. 
    Interfaces like: UART, SPI, I2C and SSH will be enabled. 
"""


def splash_screen(updater_version):
    clear_the_screen()
    print("\n\n")
    triangle_image_show()
    print(f"\t\t\t{Bcolors.BOLD} Updater version: {str(updater_version)}{Bcolors.ENDC}")
    sleep(1)


def serial_menu(config):
    ota_status = load_ota_sys_markers(config.user)

    def uart_enabling():  # UART enabling prompt is also being shown when entering nodes flash menu for the first time
        # TODO Make this repeatable without adding multiple copies at the end of config.txt.
        os.system("./scripts/sys_conf.sh uart")
        ota_status.uart_support_added = True
        write_ota_sys_markers(ota_status, config.user)
        print("""

        Serial port enabled successfully.
        You have to reboot Raspberry now,
        so changes can be implemented. Ok?



        r - Reboot now{yellow}

        e - Exit{endc}
            """.format(endc=Bcolors.ENDC, yellow=Bcolors.YELLOW_S))
        selection = input()
        if selection == 'r':
            os.system("sudo reboot")
        elif selection == 'e':
            return

    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        serial_adding_menu = """
            Serial port (UART) has to be enabled. 
            Without it Arduino-nodes cannot be programmed.
            Do you want to enable it now?



         {green}y - yes, enable UART now {endc}
     
                s - skip this prompt
            
                d - don't show this prompt again

        {yellow}a - abort{endc}
        
        
            """.format(yellow=Bcolors.YELLOW_S, green=Bcolors.GREEN_S, endc=Bcolors.ENDC)
        selection = input(serial_adding_menu)
        if selection == 'y':
            if ota_status.uart_support_added:
                print("\n\n\t\tLooks like you already enabled Serial port. \n\t\tDo you want to continue anyway?\n")
                selection = input(f"\t\t\t{Bcolors.YELLOW}Press 'y' for yes or 'a' for abort{Bcolors.ENDC}\n")
                if selection == 'y':
                    uart_enabling()
                    break
                elif selection == 'a':
                    break
            else:
                uart_enabling()
                break
        elif selection == 's':
            old_flash_gpio(config) if config.old_hw_mod else flashing_menu(config)
            break
        elif selection == 'd':
            ota_status.uart_support_added = True
            write_ota_sys_markers(ota_status, config.user)
            old_flash_gpio(config) if config.old_hw_mod else flashing_menu(config)
            break
        elif selection == 'a':
            break


def aliases_menu(config):
    ota_status = load_ota_sys_markers(config.user)

    def aliases_content():
        """load ota status, update aliases then write ota_status"""
        os.system("cat ./resources/aliases.txt | tee -a ~/.bashrc")
        ota_status.aliases_implemented = True
        write_ota_sys_markers(ota_status, config.user)
        print("\n\n\t\t    Aliases added successfully")
        sleep(2)
        return

    while True:
        clear_the_screen()
        aliases_description = f""" 
        Aliases in Linux act like shortcuts or references to another commands. 
        You can use them every time when you operates in the terminal window. 
        For example instead of typing 'python3 ~/RotorHazard/src/server/server.py' 
        you can just type 'ss' (server start) etc. Aliases can be modified and added 
        anytime you want. You just have to open '~./bashrc' file in text editor 
        - like 'nano'. After that you have reboot or type 'source ~/.bashrc'. 
        {Bcolors.BOLD}
        {read_aliases_file()}
        {Bcolors.ENDC}
            Do you want to use above aliases in your system?
            Reboot should be performed after adding those"""
        print(aliases_description)
        selection = input(f"\n\t\t\t{Bcolors.YELLOW}Press 'y' for yes or 'a' for abort{Bcolors.ENDC}\n")
        if selection == 'y':
            if ota_status.aliases_implemented:
                print("""

            Looks like you already have aliases added. 
            Do you want to continue anyway?

        """)
                selection = input(f"\t\t\t{Bcolors.YELLOW}Press 'y' for yes or 'a' for abort{Bcolors.ENDC}\n")
                if selection == 'y':
                    aliases_content()
                    break
                elif selection == 'a':
                    return
            else:
                aliases_content()
                break
        elif selection == 'a':
            return


def self_updater(config):
    def check_if_beta_user(config):
        if config.beta_tester is not False:
            ota_source_name = "beta" if config.beta_tester is True else config.beta_tester
            updater_info = f'{Bcolors.RED}' \
                           f'Source of the update is set to the "{Bcolors.UNDERLINE}{ota_source_name}{Bcolors.ENDC}{Bcolors.RED}" branch.{Bcolors.ENDC}\n'
        else:
            updater_info = ''

        return updater_info

    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        updater = """{bold}
        You can update OTA software by hitting 'u' now. It is advised step 
        before updating the RotorHazard server or before flashing nodes,
        so you can be sure you use the newest possible software.

        OTA version number is related to the {red}latest supported RotorHazard 
        stable server version{endc}{bold} and {blue}nodes firmware API number{endc}{bold} that OTA contains.
        Thanks to that you allways know is there a need to update.
        For example version {red}230{endc}{bold}.{blue}25{endc}{bold}.3a supports RotorHazard 2.3.0 stable 
        and contains nodes firmware with "API level 25".

        Self-updater will test your internet connection before every update
        and prevent update if there is no internet connection established.

        {updater_info}

            {green}u - Update OTA now{endc}

           {yellow}e - Exit to main menu{endc}
        """.format(green=Bcolors.GREEN_S, endc=Bcolors.ENDC, bold=Bcolors.BOLD, blue=Bcolors.BLUE,
                   yellow=Bcolors.YELLOW_S, red=Bcolors.RED, updater_info=check_if_beta_user(config))
        print(updater)
        selection = input()
        if selection == 'e':
            break
        elif selection == 'u':
            os.system("./scripts/updater_from_ota.sh")


def features_menu(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        features_menu_content = """

                                {rmf}FEATURES MENU{endc}{blue}{bold}


                        1 - Enable serial protocol {endc}{bold}

                        2 - Access Point and Internet 

                        3 - Show actual Pi's GPIO

                        4 - Add useful aliases

                        5 - Update OTA software {endc}{bold}

                        6 - Add external sensors 

                        7 - Create a log file{yellow}

                        e - Exit to main menu {endc}

                 """.format(bold=Bcolors.BOLD_S, underline=Bcolors.UNDERLINE, endc=Bcolors.ENDC,
                            blue=Bcolors.BLUE, yellow=Bcolors.YELLOW_S, red=Bcolors.RED_S, rmf=Bcolors.RED_MENU_HEADER)
        print(features_menu_content)
        selection = input()
        if selection == '1':
            serial_menu(config)
        elif selection == '2':
            conf_wizard_net(config)
        elif selection == '3':
            os.system("pinout")
            input("\nDone? Hit 'Enter'\n")
        elif selection == '4':
            try:
                aliases_menu(config)
            except AttributeError:
                attribute_error_handling()
        elif selection == '5':
            self_updater(config)  # todo better "wrong user name" handling and added here too
        elif selection == '6':
            external_sensors_menu(config)
        elif selection == '7':  # maybe add a general checking if username is setup right?
            log_to_dev(config)
        elif selection == 'e':
            break


def show_about(config):
    while True:
        clear_the_screen()
        welcome_first_page = """{bold}  

    Please configure OTA software using a wizard after reading this page.

    This wizard will configure OTA software, not RotorHazard server itself. 
    Things like amount of LEDs or RotorHazard password should be configured 
    separately in {blue}RotorHazard Manager{endc}{bold} - see in Main Menu.



    Possible RotorHazard server versions that may be selected:

    > {blue}'stable'{endc}{bold}- last stable release (can be from before few days or few months){endc}{bold}

    > {blue}'beta'  {endc}{bold}- last 'beta' release (usually has about few weeks, quite stable){endc}{bold}

    > {blue}'main'{endc}{bold}- absolutely newest features implemented (even if not well tested){endc} 



    {green}c - Enter configuration wizard{endc}{yellow}

           e - Exit to menu {endc}

        """.format(green=Bcolors.GREEN_S, blue=Bcolors.BLUE, endc=Bcolors.ENDC,
                   yellow=Bcolors.YELLOW_S, bold=Bcolors.BOLD)
        print(welcome_first_page)
        selection = input()
        if selection == 'c':
            config = conf_ota(config)
            break
        elif selection == 'e':
            break

    return config


def end():
    clear_the_screen()
    print("\n\n")
    ota_asci_image_show()
    print(f"\t\t\t{Bcolors.BOLD}Happy flyin'!{Bcolors.ENDC}\n")
    sleep(1.3)
    clear_the_screen()
    sys.exit()


def main_menu(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        rh_update_prompt = rh_update_check(config)
        conf_color = Bcolors.GREEN if config_check() is False else ''
        main_menu_content = """

                                {rmf}MAIN MENU{endc}

                            {blue}{bold}  
                        1 - RotorHazard Manager {rh_update_prompt} 
                            {blue}{bold}
                        2 - Nodes flash and update {endc}{bold}
                            
                        3 - Additional features{configured}

                        4 - Configuration wizard{endc}{bold}{yellow}

                        e - Exit to Raspberry OS{endc}

                """.format(bold=Bcolors.BOLD_S, underline=Bcolors.UNDERLINE, endc=Bcolors.ENDC, green=Bcolors.GREEN,
                           blue=Bcolors.BLUE, yellow=Bcolors.YELLOW_S, red=Bcolors.RED, configured=conf_color,
                           rmf=Bcolors.RED_MENU_HEADER, rh_update_prompt=rh_update_prompt)
        print(main_menu_content)
        selection = input()
        if selection == '1':
            try:
                rpi_update(config)
            except AttributeError:
                attribute_error_handling()
        elif selection == '2':
            try:
                ota_status = load_ota_sys_markers(config.user)
                if ota_status.uart_support_added:
                    old_flash_gpio(config) if config.old_hw_mod else flashing_menu(config)
                # enters "old" flashing menu only when "old_hw_mod" is confirmed
                else:
                    serial_menu(config)
            except AttributeError:
                attribute_error_handling()
        elif selection == '3':
            features_menu(config)
        elif selection == '4':
            config = show_about(config)
        elif selection == 'e':
            end()


def main():
    compatibility()
    updater_version = get_ota_version(False)
    config = load_config()
    splash_screen(updater_version)
    updated_check(config)
    ota_update_available_check(config)
    welcome_screen(config)
    main_menu(config)


if __name__ == "__main__":
    main()
