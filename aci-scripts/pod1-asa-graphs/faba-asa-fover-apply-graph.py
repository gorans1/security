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
"""
Script does a 'magic green ball' wizard which is found if you right-click on the
L4-7 service graph.  It creates an app-to-db contract, filter, and applies the
service graph to this contract for ASA firewall inspection of traffic.
This renders the service graph in the fabric by adding all config necessary for
directing traffic to ASA firewall and performing inspection dictacted by the
function profile for this L4-7 device.
"""
'''
Autogenerated code using arya
Original Object Document Input: 
'''

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.fv
import cobra.model.pol
import cobra.model.vns
import cobra.model.vz
from cobra.internal.codec.xmlcodec import toXMLStr
import sys
pod_num_start = int(sys.argv[1])
pod_num_end = int(sys.argv[2])


# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('https://10.10.35.10', 'pod%s' % pod_num_end, 'cisco')
md = cobra.mit.access.MoDirectory(ls)
md.login()
for pod_num in range(pod_num_start, (1 + pod_num_end)):
    # the top level object on which operations will be made
    polUni = cobra.model.pol.Uni('')
    #topMo = cobra.model.pol.Uni('')

    # build the request using cobra syntax
    fvTenant = cobra.model.fv.Tenant(polUni, 'pod%s' % pod_num)

    fvAp = cobra.model.fv.Ap(fvTenant, prio=u'unspecified', name=u'aprof')
    fvAEPg = cobra.model.fv.AEPg(fvAp, matchT=u'AtleastOne', name=u'app')
    fvRsCons = cobra.model.fv.RsCons(fvAEPg, tnVzBrCPName=u'app-to-db')
    fvAEPg2 = cobra.model.fv.AEPg(fvAp, matchT=u'AtleastOne', name=u'db')
    fvRsProv = cobra.model.fv.RsProv(fvAEPg2, tnVzBrCPName=u'app-to-db')
    vzBrCP = cobra.model.vz.BrCP(fvTenant, name=u'app-to-db')
    vzSubj = cobra.model.vz.Subj(vzBrCP, revFltPorts=u'yes', name=u'Subject', prio=u'unspecified', descr=u'', consMatchT=u'AtleastOne', provMatchT=u'AtleastOne')
    vzRsSubjFiltAtt = cobra.model.vz.RsSubjFiltAtt(vzSubj, tnVzFilterName=u'default')
    vzRsSubjGraphAtt = cobra.model.vz.RsSubjGraphAtt(vzSubj, tnVnsAbsGraphName=u'asa-fail-graph')
    vnsLDevCtx = cobra.model.vns.LDevCtx(fvTenant, ctrctNameOrLbl=u'app-to-db', graphNameOrLbl=u'asa-fail-graph', nodeNameOrLbl=u'Firewall')
    vnsLIfCtx = cobra.model.vns.LIfCtx(vnsLDevCtx, connNameOrLbl=u'external')
    vnsRsLIfCtxToLIf = cobra.model.vns.RsLIfCtxToLIf(vnsLIfCtx, tDn=u'uni/tn-pod%s/lDevVip-pod%s-asa-fover/lIf-external' % (pod_num, pod_num))
    vnsLIfCtx2 = cobra.model.vns.LIfCtx(vnsLDevCtx, connNameOrLbl=u'internal')
    vnsRsLIfCtxToLIf2 = cobra.model.vns.RsLIfCtxToLIf(vnsLIfCtx2, tDn=u'uni/tn-pod%s/lDevVip-pod%s-asa-fover/lIf-internal' % (pod_num, pod_num))
    vnsRsLDevCtxToLDev = cobra.model.vns.RsLDevCtxToLDev(vnsLDevCtx, tDn=u'uni/tn-pod%s/lDevVip-pod%s-asa-fover'  % (pod_num, pod_num))


    # commit the generated code to APIC
    print toXMLStr(fvTenant)
    c = cobra.mit.request.ConfigRequest()
    c.addMo(fvTenant)
    md.commit(c)

