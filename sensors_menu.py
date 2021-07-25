from modules import Bcolors, clear_the_screen, logo_top, load_config
import os

def oled_screen_menu(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        oled_menu_content = """
        
        OLED screen support will be added. 
        Do you want to continue?
        
        y - Yes
        
        a - Abort
        
        """
        print(oled_menu_content)
        selection = input()
        if selection.lower() == 'y':
            os.system(f"./home/{config.user}/RH-ota/scripts/oled_screen.sh")
            print("OLED screen libraries added")
        elif selection == 'a':
            break


def rtc_menu():
    None


def sensors_menu(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        sensors_menu_content = """

                                {rmf}SENSORS MENU{endc}{bold}


                        1 - Add OLED screen support

                        2 - Add RTC support {yellow}

                        e - Exit to previous menu {endc}

                 """.format(yellow=Bcolors.YELLOW, bold=Bcolors.BOLD_S, endc=Bcolors.ENDC, rmf=Bcolors.RED_MENU_HEADER)
        print(sensors_menu_content)
        selection = input()
        if selection == '1':
            oled_screen_menu(config)
        elif selection == '2':
            rtc_menu()
        elif selection == 'e':
            break


def main():
    config = load_config()
    sensors_menu(config)


if __name__ == "__main__":
    main()
