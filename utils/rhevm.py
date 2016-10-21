import sys
import time
import pycurl
import ovirtsdk4 as sdk
import ovirtsdk4.types as types


class RHEVM(object):
    """base class represents rhevm instance"""

    def __init__(self,
                 rhevm_fqdn,
                 rhevm_user="admin@internal",
                 rhevm_password="password",
                 ca_file="/tmp/ca.pem"):

        self.rhevm_fqdn = rhevm_fqdn
        self.api_url = "https://{0}/ovirt-engine/api".format(self.rhevm_fqdn)
        self.rhevm_user = rhevm_user
        self.rhevm_password = rhevm_password
        self.ca_file = ca_file

        self._fetch_ca_file()

        self.conn = sdk.Connection(
            url=self.api_url,
            username=self.rhevm_user,
            password=self.rhevm_password,
            ca_file=self.ca_file)

    def _fetch_ca_file(self):
        cert_url = ("https://{0}/ovirt-engine/services/"
                    "pki-resource?resource=ca-certificate"
                    "&format=X509-PEM-CA").format(self.rhevm_fqdn)

        with open(self.ca_file, "wb") as fp:
            c = pycurl.Curl()
            c.setopt(pycurl.URL, cert_url)
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.SSL_VERIFYPEER, False)
            c.setopt(pycurl.WRITEDATA, fp)
            try:
                c.perform()
            except:
                import traceback
                traceback.print_exc(file=sys.stderr)
                sys.stderr.flush()

    @property
    def hosts_service(self):
        """hosts"""
        return self.conn.system_service().hosts_service()

    @property
    def vms_service(self):
        """vms"""
        return self.conn.system_service().vms_service()


class Hosts(RHEVM):
    """This class represent host related operations

    >>> hosts = Hosts("rhevm-40-2.englab.nay.redhat.com")
    >>> r = hosts.find_host("cockpit")
    >>> print(r[1].name)
    cockpit
    >>> r2 = hosts.remove_host("cockpit")
    >>> print(r2)
    True

    """

    def hosts(self):
        """return all hosts in format
        [("id", "name", "ip"), ...]
        """
        host_list = self.hosts_service.list()
        return [(h.id, h.name, h.address) for h in host_list if host_list]

    def add_host(self,
                 name,
                 address,
                 wait_host_up=False,
                 description="for automation testing use",
                 root_password="redhat",
                 cluster_name="Default"):

        host_ = types.Host(
            name=name,
            description=description,
            address=address,
            root_password=root_password,
            cluster=types.Cluster(
                name=cluster_name,
            ),
        )
        host = self.hosts_service.add(host_)

        if wait_host_up:
            h = self.hosts_service.host_service(host.id)

            timeout = time.time() + 60 * 5  # 5 minutes from now
            while True:
                time.sleep(5)
                ret = h.get()

                if ret.status == types.HostStatus.UP or time.time() > timeout:
                    print("Add host finished or is timeout")
                    break

    def find_host(self, name):
        hosts_ = self.hosts_service.list(search=name)
        if hosts_:
            for h in hosts_:
                if h.name == name:
                    return h.id, h
            return False, False
        else:
            return False, False

    def remove_host(self, name):
        host_id, host = self.find_host(name)
        if not host_id:
            print("can not found host {0}".format(name))
            return False

        host_service = self.hosts_service.host_service(host_id)
        if host.status != types.HostStatus.MAINTENANCE:
            host_service.deactivate()
        host_service.remove()
        return True

    def __del__(self):
        self.conn.close()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
