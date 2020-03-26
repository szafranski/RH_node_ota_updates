from time import sleep
import os
from modules import clear_the_screen, Bcolors, logo_top, write_json
from pathlib import Path

'''
Check if a config file already exists. if it does, 
ask the user if they want to overwrite it.
'''


def conf_check():
    conf_now_flag = 0
    if os.path.exists("./updater-config.json"):
        print("\n\tLooks that you have OTA software already configured.")
        valid_options_conf_check = ['y', 'yes', 'n', 'no']
        while True:
            cont_conf = input("\n\tOverwrite and continue anyway? [yes/no]\t\t").strip()
            if cont_conf in valid_options_conf_check:
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
        if cont_conf[0] == 'y':
            conf_now_flag = 1
        if cont_conf[0] == 'n':
            conf_now_flag = 0
            breakpoint()
    else:
        conf_now_flag = 1
    return conf_now_flag


def do_config():
    home_dir = str(Path.home())
    clear_the_screen()
    logo_top(False)

    # Always define variables before using them.

    conf_now_flag = conf_check()

    if conf_now_flag:
        config = {}

        print("""\n
Please type your configuration data. It can be modified later.
Default values are not automatically applied. Type them if needed.\n""")
        name = input("\nWhat is your user name on Raspberry Pi? [default: pi]\t\t\t")
        config['pi_user'] = name
        while True:
            version = input(f"\nWhat RotorHazard version will you use? \
[{Bcolors.UNDERLINE}stable{Bcolors.ENDC} | beta | master]\t\t")
            version_valid_options = ['master', 'stable', 'beta']
            if version not in version_valid_options:
                print("\nPlease enter correct value!")
            else:
                config['RH_version'] = version
                break

        debug_user = input("\nWhat is you user name on debugging OS? [default: racer]\t\t\t")
        config['debug_user'] = debug_user

        code = input("\nWhat is your country code? [default: GB]\t\t\t\t")
        config['country'] = code

        while True:
            nodes = input("\nHow many nodes will you use in your system? [min: 0/1 | max: 8]\t\t")
            if not nodes.isdigit() or int(nodes) > 8:
                print("\nPlease enter correct value!")
            else:
                config['nodes_number'] = nodes
                break

        while True:
            debug_mode = input("\nWill you use \"OTA\" software in a debug mode? [yes/no | default: no]\t")
            debug_mode_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if debug_mode not in debug_mode_allowed_values:
                print("\nPlease enter correct value!")
            else:
                debug_mode_val = '0'
                if debug_mode in ['yes', '1', 'y']:
                    debug_mode_val = '1'
                elif debug_mode in ['no', '0', 'n']:
                    debug_mode_val = '0'
                config['debug_mode'] = debug_mode_val
                break
        while True:
            pins_assign = input("\nPins assignment? [default/custom/PCB | default: default]\t\t")
            pins_valid_options = ['default', 'PCB', 'pcb', 'custom']
            if pins_assign not in pins_valid_options:
                print("\nPlease enter correct value!")
            else:
                config['pins_assignment'] = pins_assign
                break

        while True:
            no_pdf_val = '0'
            no_pdf = input("\nUpdates without PDF? [yes/no | default: yes]\t\t\t\t")
            no_pdf_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if no_pdf not in no_pdf_allowed_values:
                print("\nPlease enter correct value!")
            else:
                if no_pdf in ['yes', '1', 'y']:
                    no_pdf_val = '1'
                elif no_pdf in ['no', '0', 'n']:
                    no_pdf_val = '0'
                config['updates_without_pdf'] = no_pdf_val
                break

        while True:
            pi_4 = input("\nAre you using Raspberry Pi 4? [yes/no | default: no]\t\t\t")
            pi_4_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if pi_4 not in pi_4_allowed_values:
                print("\nPlease enter correct value!")
            else:
                pi_4_val = '0'
                if pi_4 in ['yes', '1', 'y']:
                    pi_4_val = '1'
                elif pi_4 in ['no', '0', 'n']:
                    pi_4_val = '0'
                config['pi_4_cfg'] = pi_4_val
                break

        while True:
            beta_tester = input("\nAre you a beta tester? [yes/no | default: no]\t\t\t\t")
            beta_tester_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if beta_tester not in beta_tester_allowed_values:
                print("\nPlease enter correct value!")
            else:
                beta_tester_val = '0'
                if beta_tester in ['yes', '1', 'y']:
                    beta_tester_val = '1'
                elif beta_tester in ['no', '0', 'n']:
                    beta_tester_val = '0'
                config['beta_tester'] = beta_tester_val
                break

        print(f"""\n\n
            {Bcolors.UNDERLINE}CONFIGURATION{Bcolors.ENDC}:

        User name:              {name}
        RotorHazard version:    {version}
        Debug user name:        {debug_user}
        Country code:           {code}
        Nodes amount:           {nodes}
        Debug mode:             {debug_mode}    
        Pins assignment:        {pins_assign}
        Updates without PDF:    {no_pdf}
        Pi 4 user:              {pi_4}
        Beta tester:            {beta_tester}
         
        Please check. Confirm? [yes/change/abort]\n""")
        valid_options = ['y', 'yes', 'n', 'no', 'change', 'abort']
        while True:
            selection = input().strip()
            if selection in valid_options:
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
        if selection == 'y' or selection == 'yes':
            write_json(config, f"{home_dir}/RH-ota/updater-config.json")

            print("Configuration saved.\n")
            sleep(0.5)
            conf_now_flag = 0
        if selection in ['change', 'n', 'no']:
            conf_now_flag = 1
        if selection == 'abort':
            print("Configuration aborted.\n")
            sleep(0.5)
            conf_now_flag = 0

    return conf_now_flag


def conf_ota():
    """
        repeat the configuration script until
        the user ether aborts, configures ota
        or it was already configured.
    :return:
    """
    config_now = 1
    while config_now:
        config_now = do_config()


def main():
    conf_ota()


if __name__ == "__main__":
    main()
