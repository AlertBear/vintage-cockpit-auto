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

    headers = {
        "Prefer": "persistent-auth",
        "Accept": "application/json",
        "Content-type": "application/xml"
    }

    cert_url = ("https://{rhevm_fqdn}/ovirt-engine/services"
                "/pki-resource?resource=ca-certificate&format=X509-PEM-CA")

    rhevm_cert = "/tmp/rhevm.cert"

    new_host_post_body = '''
    <host>
        <name>{host_name}</name>
        <address>{ip}</address>
        <root_password>{password}</root_password>
    </host>
    '''

    new_storage_post_body = '''
    <storage_domain>
      <name>{storage_name}</name>
    </storage_domain>
    '''

    def __init__(self,
                 rhevm_fqdn,
                 user="admin",
                 password="password",
                 domain="internal"):

        self.rhevm_fqdn = rhevm_fqdn
        self.user = user
        self.password = password
        self.domain = domain
        self.token = base64.b64encode(
            self.auth_format.format(
                user=self.user, domain=self.domain, password=self.password))
        self.headers.update({
            "Authorization": "Basic {token}".format(token=self.token)
        })
        self._get_rhevm_cert_file()
        self.req = requests.Session()

    def _get_rhevm_cert_file(self):
        r = requests.get(self.cert_url.format(rhevm_fqdn=self.rhevm_fqdn),
                         stream=True,
                         verify=False)

        if r.status_code == 200:
            with open(self.rhevm_cert, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            raise RuntimeError("Can not get the cert file from %s" %
                               self.rhevm_fqdn)

    def query_host_id_by_name(self, host_name):
        api_url = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item="hosts")

        r = self.req.get(api_url, headers=self.headers, verify=self.rhevm_cert)
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
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item='hosts')
        api_url = api_url_base + "/%s/deactivate" % host_id
        # print api_url
        r = self.req.post(
            api_url,
            headers=self.headers,
            verify=self.rhevm_cert,
            data="<action/>")
        ret = r.json()
        if ret['status'] != 'complete':
            raise RuntimeError(ret['fault']['detail'])

    def add_new_host(self, *rhvh_credentials):
        ip, host_name, password = rhvh_credentials
        api_url = self.api_url.format(rhevm_fqdn=self.rhevm_fqdn, item="hosts")
        body = self.new_host_post_body.format(
            host_name=host_name, ip=ip, password=password)

        r = self.req.post(
            api_url, data=body, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 201:
            print r.text
            raise RuntimeError(
                "Failed to add new host, may be host already imported")

    def remove_host(self, host_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="hosts")
        host_id = self.query_host_id_by_name(host_name)

        if host_id:
            self._deactive_host(host_id)
            time.sleep(5)
            api_url = api_url_base + '/%s' % host_id

            r = self.req.delete(
                api_url, headers=self.headers, verify=self.rhevm_cert)
            if r.status_code != 200:
                raise RuntimeError("Can not delete host %s" % host_name)
        else:
            print "Can't find host with name %s" % host_name

    def attach_storage_to_datacenter(self, storage_name, dc_name):
        api_url_base = self.api_url.format(
            rhevm_fqdn=self.rhevm_fqdn, item="datacenters")
        api_url = api_url_base + '/%s/storagedomains' % dc_name

        body = self.new_storage_post_body.format(storage_name=storage_name)

        r = self.req.post(
            api_url, data=body, headers=self.headers, verify=self.rhevm_cert)

        if r.status_code != 201:
            print r.text
            raise RuntimeError("Failed to attach storage %s to datacenter %s" %
                               (storage_name, dc_name))
