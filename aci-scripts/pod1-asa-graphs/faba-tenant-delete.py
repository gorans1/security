#!/usr/bin/env python
################################################################################
#                                                                              #
# Copyright (c) 2017 Cisco Systems                                             #
# All Rights Reserved.                                                         #
#                                                                              #
#    Licensed under the Apache License, Version 2.0 (the "License"); you may   #
#    not use this file except in compliance with the License. You may obtain   #
#    a copy of the License at                                                  #
#                                                                              #
#         http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                              #
#    Unless required by applicable law or agreed to in writing, software       #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################
"""  This script deletes specific items in the pod# (i.e. pod1) tenant, allowing
     user to get re-create them with out overlapping configurations.
"""

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.fv
import cobra.model.pol
import cobra.model.vz
from cobra.internal.codec.xmlcodec import toXMLStr
import sys
pod_num_start = int(sys.argv[1])
pod_num_end = int(sys.argv[2])

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.10.35.10',  'pod%s' % pod_num_end, 'cisco')
md = cobra.mit.access.MoDirectory(ls)
md.login()
for pod_num in range(pod_num_start, (1 + pod_num_end)):
    # Remove asa-clu service graph from contract
    item = md.lookupByDn("uni/tn-pod%s/brc-out-to-web/subj-Subject/rsSubjGraphAtt" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete application profile
    item = md.lookupByDn("uni/tn-pod%s/ap-aprof" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete internal VRF pod#net
    item = md.lookupByDn("uni/tn-pod%s/ctx-pod%snet" % (pod_num,pod_num))
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete external VRF vrf#net
    item = md.lookupByDn("uni/tn-pod%s/ctx-vrf%snet" % (pod_num,pod_num))
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete external L3out for ASA context on ASA cluster
    item = md.lookupByDn("uni/tn-pod%s/out-asa-clu-external" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete internal L3out for ASA context on ASA cluster
    item = md.lookupByDn("uni/tn-pod%s/out-asa-clu-internal" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete WAN L3out (fabric to outside) 
    item = md.lookupByDn("uni/tn-pod%s/out-wan-out" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete app Bridge Domain
    item = md.lookupByDn("uni/tn-pod%s/BD-app" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete db Bridge Domain
    item = md.lookupByDn("uni/tn-pod%s/BD-db" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete web Bridge Domain
    item = md.lookupByDn("uni/tn-pod%s/BD-web" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete app-to-db contract
    item = md.lookupByDn("uni/tn-pod%s/brc-app-to-db" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete out-to-web contract
    item = md.lookupByDn("uni/tn-pod%s/brc-out-to-web" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete asa-clu-graph service graph template
    item = md.lookupByDn("uni/tn-pod%s/AbsGraph-asa-clu-graph" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete asa-fail-graph service graph template
    item = md.lookupByDn("uni/tn-pod%s/AbsGraph-asa-fail-graph" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete asa-clu-gr function profile (ASA config in APIC)
    item = md.lookupByDn("uni/tn-pod%s/absFuncProfContr/absFuncProfGrp-asa-clu-gr" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete asa-fail-gr function profile (ASA config in APIC)
    item = md.lookupByDn("uni/tn-pod%s/absFuncProfContr/absFuncProfGrp-asa-fail-gr" % pod_num)
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete asa-cluster context L4-L7-device
    item = md.lookupByDn("uni/tn-pod%s/lDevVip-pod%s-asa-clu" % (pod_num,pod_num))
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)

    # Delete asa-failover context L4-L7-device
    item = md.lookupByDn("uni/tn-pod%s/lDevVip-pod%s-asa-fover" % (pod_num,pod_num))
    item.delete()
    print toXMLStr(item)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(item)
    md.commit(c)
