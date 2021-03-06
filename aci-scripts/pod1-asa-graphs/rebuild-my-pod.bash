#!/bin/bash
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
This script is a wrapper for all python scripts that allow us to take our 
tenant re-build in step by step fashion.        
"""
#
#
path=""
for i in (1..1)
   do
   echo " Delete pod$i tenant items (app profile,EPGs,BDs,contract,l3outs,vrfs,L4-L7 items:  [continue]"; read go
   python ${path}faba-tenant-delete.py $i $i
   echo " Create pod$i tenant app profile, EPGs, vrfs, BDs:  [continue]"; read go
   python ${path}faba-tenant-apps.py $i $i
   echo " Create asa failover context as L4-L7 device: [continue]"; read go

   python ${path}faba-asa-fover-pods.py $i $i
   echo " Create context config - function profile: [continue]"; read go
   python ${path}faba-asa-fover-fprof.py $i $i
   echo " Add service graph: [continue]"; read go
   python ${path}faba-asa-fover-graph.py $i $i
   echo " Apply asa-fover SG and create app-to-db contract: [continue]"; read go
   python ${path}faba-asa-fover-apply-graph.py $i $i
   echo " Create asa cluster context as L4-L7 device: [continue]"; read go
   python ${path}faba-asa-cluster-pods-new.py $i $i
   
   echo " Create context config - function profile: [continue]"; read go
   python ${path}faba-asa-cluster-fprof.py $i $i
   echo " Add service graph: [continue]"; read go
   python ${path}faba-asa-cluster-graph.py $i $i
   echo " Create L3outs for fabric and ASA cluster context: [continue]"; read go
   python ${path}faba-l3out.py $i $i
   echo " Apply asa-cluster SG and create out-to-web contract: [continue]"; read go
   python ${path}faba-asa-cluster-apply-graph.py $i $i
   echo " We are done, now review pod$i tenant and ping out->web and app->db: [continue]"; read go
   done
