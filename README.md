Password Security Tool

I made a program using python for account registration and login.
The main idea is to explore core password security concepts;
including salted hashing, account lockout and password strength checks.
First, I built it as a command-line tool , I then rebuilt it with a Tkinter GUI.


FEATURES:
1) Password security:
-password strength checks based on 5 criteria.
-minimum password score with a 3/5 score requirement.
-checks for:
            At least 8 characters , 
            Uppercase and  lowercase letters,
            A number and atleast one special character.
-password conformation during registration.
-a random salt generated for each password
-SHA-256 password hashing
-passwors not stored in plaintext




2) Account lockout after 3 failed login attempts, with a live "attempts remaning" counter.




3) Admin unlock to reset a locked account.



4) Security audit log (security_log.txt) recording registrations, logins, failed attempts, and lockouts with timestamps



DESIGN DECISIONS:



1)Salting before hashing — prevents identical passwords from producing identical hashes.


2)Lockout — a basic defence against brute-force login guessing.


3)Audit log — every registration, login, failed attempt, and lockout is timestamped and logged, so account activity can be reviewed.


4)Password strength scoring — gives the user immediate feedback rather than a hard binary accept/reject, while still enforcing a minimum bar (3/5 checks) before allowing registration.
 

NEXT STAGES:


1)Hashing algorithm — currently uses raw SHA-256, which is designed to be fast. That's the wrong property for password hashing, since it makes brute-forcing a stolen hash cheap. 
  A slow, purpose-built KDF like PBKDF2, bcrypt, or Argon2 (with a high iteration count) would be the correct choice.



2)Hardcoded admin unlock code — the admin code currently lives as a plaintext string in the source file. 
  It should be loaded from an environment variable or an external config file that isn't committed to version control.




3)Username enumeration — an incorrect username doesn't currently count against the login attempt limit, so usernames could be brute-forced separately from password.





WHAT I LEARNED:


I learned about Python and practical password security through research, AI-assisted learning, testing and debugging. 
I learned how to use tools such as hashlib for hashing, secrets for salts, getpass for hidden password input, json for data storage and datetime for timestamps. 
I also learned why hashing, salting and account lockouts are important for protecting user accounts.