```python

''' manual prechecks
0- is ping count 1 and ssh successful ask for router hostname from NSO server  | ping ssh
1- device illegal refrence | device is not available in cfs | Onboard in CFS
2- device not in any contoller | device is not onboarded in nso rfs | Onboarded in RFS
3- authentication issues | fail to connect | fail to connect
4- fail to connect | may be ssh fetch-host-key to be done | fail to connect
                     then sync-from
5- out-of sync | pls sync the device

6- onboard the device in cfs
7- onboard the device in rfs

8 is the same ip device is already onboarded in nso and now due to ring change happen 
  hostname has been changed.
  
  is onboarded router hostname and NSO onboarded hostname same?
  that logic can be applied to check the ring change happend or not
  
  
'''
```
