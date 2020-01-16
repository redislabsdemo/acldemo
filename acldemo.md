# Demo of Access Control Lists in Redis Open Source 6.0 Release Candidate

## Leveraging A Demo Home Furniture and Goods Site Backend - Demo Script
Data load script: src/oss-acls/loaddata.sh
### Step 0: Prepare environment leveraging the preparation script above.

```shell
#/bin/bash
sudo sudo apt update -y
sudo apt install build-essential tcl -y
sudo apt install tcl-tls -y
sudo apt install redis-tools -y
git clone https://github.com/antirez/redis.git
cd ./redis
make
./src/redis-server
git clone https://github.com/redislabsdemo/acldemo.git
cd ./acldemo
chmod +x ./loaddata.sh
./loaddata.sh
```
### Step 1: Try to login as the default user

So lets get started by logging into Redis. Redis now comes with a default user, "default" who by default comes with no password. It is best security practice to always set this users password or disable it by default.

```shell
> auth default nopass 
```
Notice the default ACL user is not able to log in. Thats because as part of this demo the user has been disabled. We can enable it with the user admin.

### Step 2: Demonstrate user restriction best practice patterns. 

A common enterprise pattern is to allow an admin user with no access to data to provision all users. We have provisioned one of these users to assist us in the event we ever need to troubleshoot and enable the default user. Lets do that now.

```shell
> auth admin password
> ACL LIST
```
The admin user has access to a list of users within the redis database. As you can see the passwords are stored in protected by hashes. Commands can be restricted using the '+' and '-' operator as part of the ACL command. Categories of commands such as read, write or admin are denoted with the '@' operator, as you can see in the admin users permissions, the @admin category of commands is given to this user where only specific commands are provided to other users. 

Keys within the redis database can be added with the '~' operator in a glob style wildcard pattern. Lets add a user now to demonstrate


```shell
> ACL SETUSER itamar on #B800CDA07DB0CB1C97227E5CC9BF51084F414B1BB7F43264D701C9D526DA5539 +hget +get +@admin ~secret:* ~public:*
```
What we are doing here is creating a user itamar with the password 'itamarwashere' and assigning itamar access to any key assigned with the secret or public label on the key.

ACL passwords can be added with the '>' for cleartext passwords or the # denotation for hashed passwords in the event that you do not actually know the password or are running scripts from a logged location where you do not want to log passwords. All hashes must be SHA-256 hashes. If added directly inside the redis-cli any password will not be logged.

**Its important to never disable the default user without putting another ACL user with @admin or +acl permissions on the database at a minimum.**

The default user is able to disable itself and you will not be able to log back in after the client session ends. To learn more about ACLs visit https://redis.io/topics/acl

### Step 3: Demonstrate Key Design Patterns.

The demonostration database hosts keys for an application that can be used for the tracking of users who purchase goods on a home goods ecommerce site. Users login with their username and password, enter information about themselves and purchase home goods & furniture.

```shell
SCAN 0 COUNT 30
```

These keys have all been labeled with their data classification as their ACL label. Using ACL Labels can be used as a means of restricting ACL users from specific label types. Labels can be used as a means of enforcing a form of role based access control where a label or set of labels is equivalent to a role. In addition to labels key restrictions can also be put at an object level to provide granular access to key object types. This is entirely dependent on your Key Design strategy. This database was designed using a labeling strategy.


Its important to note the design of the keys. Key Design is a fundamental tenant of ACLs. **The below labels are not intended to be perscriptive but shows label categorization in action.** Lets explore it below.

1. public: Denotes data that is not sensitive that will not have a major impact if unauthorized read access occurs.
2. secret: Denotes data that is sensitive to customers and requires sensitivity in access controls. 
3. topsecret: Denotes data that you would not typically want users to access such as user passwords and password hashes.

Lets dig into how key labels can be used to assign permissions to ACL users in Redis.

```shell
ACL LIST
```

Lets observe the permissions of the users below. 

* serviceacct2 has access to the topsecret keys label and the ability to set and get on those keys.
* serviceacct has the ability ot hset, hget and hgetall on keys with the secret label
* serviceacct3 has the ability to set, get, hset, hget and hgetall on keys with the public label.
* user1 has only read permissions to set and hget on keys labeled with the public label.

We have just made itamar and admin is used only to set ACL users on the database and perform other administrative functions.

Lets demonstrate key label access restrictions in action.

### Step 4: Demonstrate Key Pattern Restrictions

First we will login as the serviceacct user who has access to secret key labels.

```shell
AUTH serviceacct password2
```
We can access user:16's data because it has the secret tag using the following commands:

```shell
hgetall secret:users:16
hget secret:users:16 ccn 
```
However, we can not access the orders object because it has the public label, which serviceacct does not have access to.

```shell
hget public:order:1 
```

We would have to use serviceacct3 or user1 in order to access the order details.

#### Step 5: Demonstrate Command Restrictions

Service accounts can also be designed to only be able to access the keys and commands they need to operate for their given application design. Lets login to user1 to demonstrate. If you are designing a database with only gets and sets you should probably not give hget to any users. Administrators can also restrict commands in a blacklist rather than a whitelist as this demo shows.


```shell
AUTH user1 password1
```

Lets see that order our service account was unable to access earlier.

```shell
hget public:order:1 item
hget public:order:1 user
```

We can see here that the user can read public labels to see that user 2 ordered a table. Lets see what happens if we try to modify this order.

```shell
hset public:order:1 item pumpkin
```

Because user1 has no need to modify orders because that would be done by our service account this has been blocked by our ACL command restrictions. +@all can be used to assign a user all access to commands.
