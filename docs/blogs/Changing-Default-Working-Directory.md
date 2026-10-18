As we know every time we login a Linux server, we will be landed in `~` directory, a.k.a the one pointed by `HOME` variable.
What if my mostly used directory is not `~`, and I want to change the initial working directory as the moment logging in because I don't want to change it every time without touching the `HOME` variable, since many trivial problems will follow like the `PATH`.

Yes, it's easy. Simply add `cd /path/to/your/work` into `~/.bashrc`.

But you would find that every time you run `bash` inside bash or just run `source ~/.bashrc` maybe for updating some settings, the working directory will change. Such side effects are not what we want.

So let's put the `cd` into `~/.profile`, where it would only be executed when you opening up a new session. Operations on current session shell won't be affected no longer.