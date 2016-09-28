import base64
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
               "Accept": "application/xml",
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

    def remove_host(self):
        raise NotImplementedError


if __name__ == '__main__':
    pass
