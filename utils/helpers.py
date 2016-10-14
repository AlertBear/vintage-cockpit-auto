import base64
import time
import requests
import shutil


class RhevmAction:
    """a rhevm rest-client warpper class
    currently can registe a rhvh to rhevm
    example:
    RhevmAction("rhevm-40-1.englab.nay.redhat.com").add_new_host("10.66.8.217", "autotest01", "redhat")
    """

    auth_format = "{user}@{domain}:{password}"
    api_url = "https://{rhevm_fqdn}/ovirt-engine/api/{item}"

    headers = {"Prefer": "persistent-auth",
               "Accept": "application/json",
               "Content-type": "application/xml"}

    cert_url = "https://{rhevm_fqdn}/ovirt-engine/services/pki-resource?resource=ca-certificate&format=X509-PEM-CA"

    rhevm_cert = "/tmp/rhevm.cert"

    new_host_post_body = '''
    <host>
        <name>{host_name}</name>
        <address>{ip}</address>
        <root_password>{password}</root_password>
    </host>
    '''

    create_nfs_post_body = '''
    <storage_domain>
        <name>nfs2</name>
        <type>data</type>
        <storage>
            <type>nfs</type>
            <address>{ip}</address>
            <path>{path}</path>
        </storage>
        <host>
            <name>{host_name}</name>
        </host>
    </storage_domain>
    '''

    attach_storage_to_datacenter_post_body='''
    <storage_domain>
      <name>nfs2</name>
    </storage_domain>
    '''

    create_vm_post_body='''
    <vm>
        <name>{vm_name}</name>
        <cluster>
            <name>default</name>
        </cluster>
        <template>
            <name>Blank</name>
        </template>
        <memory>536870912</memory> 
        <os>
            <boot dev="hd"/>
        </os>
    </vm>
    '''

    create_vm_nic_post_body='''
    <nic>
      <name>nic1</name>
      <network>
        <name>ovirtmgmt</name>
      </network>
    </nic>
    '''

    def __init__(self,
                 rhevm_fqdn,
                 user="admin", password="password", domain="internal"):

        self.rhevm_fqdn = rhevm_fqdn
        self.user = user
        self.password = password
        self.domain = domain
        self.token = base64.b64encode(self.auth_format.format(user=self.user,
                                                              domain=self.domain,
                                                              password=self.password))
        self.headers.update({"Authorization": "Basic {token}".format(token=self.token)})
        self._get_rhevm_cert_file()
        self.req = requests.Session()

    def _get_rhevm_cert_file(self):
        r = requests.get(self.cert_url.format(rhevm_fqdn=self.rhevm_fqdn),
                         stream=True, verify=False)

        if r.status_code == 200:
            with open(self.rhevm_cert, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            raise RuntimeError("Can not get the cert file from %s" % self.rhevm_fqdn)

    def query_host_id_by_name(self, host_name):
        api_url = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item="hosts")

        r = self.req.get(api_url,
                         headers=self.headers,
                         verify=self.rhevm_cert)
        if r.status_code != 200:
            raise RuntimeError("Can not list hosts from %s" % self.rhevm_fqdn)

        hosts = r.json()
        
        if hosts:
            for host in hosts['host']:
                if host['name'] == host_name:
                    return host['id']
        else:
            return False

    def _deactive_host(self, host_id):
        api_url_base = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item='hosts')
        api_url = api_url_base + "/%s/deactivate" % host_id
        # print api_url
        r = self.req.post(api_url,
                          headers=self.headers,
                          verify=self.rhevm_cert,
                          data="<action/>")
        ret = r.json()
        if ret['status'] != 'complete':
            raise RuntimeError(ret['fault']['detail'])

    def add_new_host(self, *rhvh_credentials):
        ip, host_name, password = rhvh_credentials
        api_url = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item="hosts")
        body = self.new_host_post_body.format(host_name=host_name, 
                                              ip=ip,
                                              password=password)

        r = self.req.post(api_url,
                          data=body,
                          headers=self.headers,
                          verify=self.rhevm_cert)

        if r.status_code != 201:
            print r.text
            raise RuntimeError("Failed to add new host, may be host already imported")

        time.sleep(3*60)
        r_2 = self.req.get(api_url,
                         headers=self.headers,
                         verify=self.rhevm_cert)
        ret = r_2.json()
        # while ret['host'][1]['status'] != 'up':
        #     r_2 = self.req.get(api_url,
        #                  headers=self.headers,
        #                  verify=self.rhevm_cert)
        #     ret = r_2.json()
        #     print ret['host'][1]['status']
        #     time.sleep(5)
        
        if ret['host'][1]['status'] == 'up':
            return True
        elif ret['host'][1]['status'] == 'Non Responsive':
            return False

    def remove_host(self, host_name):
        api_url_base = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item="hosts")
        host_id = self.query_host_id_by_name(host_name)

        if host_id:
            self._deactive_host(host_id)
            time.sleep(5)
            api_url = api_url_base + '/%s' % host_id

            r = self.req.delete(api_url, headers=self.headers, verify=self.rhevm_cert)
            if r.status_code != 200:
                raise RuntimeError("Can not delete host %s" % host_name)
        else:
            print "Can't find host with name %s" % host_name

    def add_nfs_data_storage(self, *rhvh_nfs):
        ip, path, host_name = rhvh_nfs     
        api_url = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item="storagedomains")
        body = self.create_nfs_post_body.format(ip=ip,
                                             path=path, 
                                             host_name=host_name)

        r = self.req.post(api_url,
                          data=body,
                          headers=self.headers,
                          verify=self.rhevm_cert)
        
        if r.status_code != 201:
            print r.text
            raise RuntimeError("Failed to add nfs storage, may be it already imported")

        self.attach_nfs_storage_to_datacenter()
        time.sleep(1.5*60)
        r_2 = self.req.get(api_url,
                         headers=self.headers,
                         verify=self.rhevm_cert)
        ret = r_2.json()
        # while ret['storage_domain'][1]['status'] != 'Active':
        #     r_2 = self.req.get(api_url,
        #                  headers=self.headers,
        #                  verify=self.rhevm_cert)
        #     ret = r_2.json()
        # print ret['storage_domain'][1]['status']
        #     time.sleep(5)
        print ret['storage_domain'][1]['status']
        if ret['storage_domain'][1]['status'] == 'Active':
            return True
        elif ret['storage_domain'][1]['status'] == 'unattached':
            return False

    def attach_nfs_storage_to_datacenter(self):
        dc_id = self.query_dc_id()
        item_string = "datacenters/" + dc_id + "/storagedomains"
        api_url = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item=item_string)
        body = self.attach_storage_to_datacenter_post_body.format()

        r = self.req.post(api_url,
                          data=body,
                          headers=self.headers,
                          verify=self.rhevm_cert)

        if r.status_code != 201:
            print r.text
            raise RuntimeError("Fail to attach nfs storage, may be it already attached")

    def query_dc_id(self):
        api_url = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item="datacenters")

        r = self.req.get(api_url,
                         headers=self.headers,
                         verify=self.rhevm_cert)
        if r.status_code != 200:
            raise RuntimeError("Can not list hosts from %s" % self.rhevm_fqdn)

        dcs = r.json()
        
        if dcs:
            for dc in dcs['data_center']:
                if dc['name'] == 'Default':
                    return dc['id']
        else:
            return False

    def create_vm(self, vm_name):    
        api_url = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item="vms")
        print api_url
        body = self.create_vm_post_body.format(vm_name=vm_name)
        print body

        r = self.req.post(api_url,
                          data=body,
                          headers=self.headers,
                          verify=self.rhevm_cert)
        
        print r.status_code

if __name__ == '__main__':
    ra = RhevmAction("rhevm-40-1.englab.nay.redhat.com")
    ra.create_vm('vm_1')
