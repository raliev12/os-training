import argparse

import libvirt

class LibvirtConn:
    def __init__(self):
        self.conn = libvirt.open("qemu:///system")

    def find_vm_dec(func):
        def closure(self, name, *args, **kwargs):
            vm = self.conn.lookupByName(name)
            return func(self, name, vm, *args, **kwargs)
        return closure

    def create_vm(self, xml_file):
        with open(xml_file) as f:
            xml = f.read()
        self.conn.defineXML(xml)

    @find_vm_dec
    def delete_vm(self, name, vm):
        if vm.isActive():
            vm.destroy()
        vm.undefine()

    @find_vm_dec
    def power_on(self, name, vm):
        vm.create()

    @find_vm_dec
    def power_off(self, name, vm):
        vm.shutdown()

    @find_vm_dec
    def reboot(self, name, vm):
        vm.reboot()


def lvirt_parse__args():
    parser = argparse.ArgumentParser(description="Pythonic wrapper "
        "for libvirt. Author: Ruslan Aliev")
    parser.add_argument('--create', dest='xml_file', metavar='VM_NAME',
        help='Create VM defined in XML_FILE')
    parser.add_argument('--delete', dest='name_del', metavar='VM_NAME',
        help='Delete VM')
    parser.add_argument('--power-on', dest='name_on', metavar='VM_NAME',
        help='Power ON VM')
    parser.add_argument('--power-off', dest='name_off', metavar='VM_NAME',
        help='Power OFF VM')
    parser.add_argument('--reboot', dest='name_reboot', metavar='VM_NAME',
        help='Reboot VM')
    return parser.parse_args()

def lvirt_exec(args):
    try:
        lvirt = LibvirtConn()
        if args.xml_file:
            lvirt.create_vm(args.xml_file)
        elif args.name_del:
            lvirt.delete_vm(args.name_del)
        elif args.name_on:
            lvirt.power_on(args.name_on)
        elif args.name_off:
            lvirt.power_off(args.name_off)
        elif args.name_reboot:
            lvirt.reboot(args.name_reboot)
        else:
            print "No options specified. Use -h for help"
    except libvirt.libvirtError, le:
        raise SystemExit(le.get_error_code())

if __name__ == '__main__':
    lvirt_exec(lvirt_parse__args())

