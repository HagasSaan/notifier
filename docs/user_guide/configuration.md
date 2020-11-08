# How to configure notifications
1. Create users, which will be used in configurations. 
<details>
  <summary>User's additional info field</summary>
    Additional info used to pass info to producers and consumers. 
    Check out documentation for every producer\consumer which you going to use.
</details>
2. Create producer(s), which will produce messages for your configuration
3. Create consumer(s), which will consume messages from your consumer
4. Select filters for excluding messages which not needed to be sent.
5. Create configuration with unique name, with any number of users, producers, consumers.
6. Configuration can be run with action in admin (Run selected configuration). 
<details>
  <summary>Logs info</summary>
  Logs of running configuration can be found in logs of workers containers, 
  or in web container if server configured in SYNC_MODE
</details>

# How to schedule configuration
1. Create configuration first.
2. Click `schedule configuration` button in admin panel
3. Configure schedule. Scheduling very similar as cron configuration
