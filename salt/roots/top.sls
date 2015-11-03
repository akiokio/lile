# top.sls

# To debug provisioning, run in the minion
# $ sudo salt-call -l debug state.highstate

base:
  '*':
    - dependencies
    - nginx
    - postgres
#    - project #Enable this to customize your workflow, if you're not familiar with salt just disable
#  'lile-dev':
#    - local-project