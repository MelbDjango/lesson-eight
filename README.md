# MelbDjango School Lesson Six

### Assignment 1

**Important:** Check out our first assignment here: https://github.com/melbdjango/melbdjango-assignment

---


Congratulations, you've made it to the git repository for our fifth lesson. Hopefully you also made it to the class and some of this makes sense to you.

Check our RESOURCES.md for some links we think you'll find handy.


## Homework Checklist

- [ ] [Fork this repository][gh-fork]
- [ ] Clone the repo to your own machine
- [ ] Use the virtualenv you created in previous lesson
- [ ] Add tests for the views using the Django's test client
- [ ] Bonus 1: Add tests to check for the string representation of your model instances
- [ ] Bonus 2: Add separate tests for the forms
- [ ] Super Bonus 3: Use [factory_boy](https://factoryboy.readthedocs.org/) to create factories for our models that can be used to simplify our tests.

When you've completed some or all of the homework please make a [Pull Request][gh-pr] against this repository. If you submit your work before Wednesday evening we'll give you feedback before the next class.

If you'd like help, make a Pull Request with your incomplete work and ask a question to @darrenfrenkel, @sesh, @funkybob or @MarkusH


## Displaying the class slides

Install reveal-md with npm and use that to display the class slides.

```
    npm install -g reveal-md
```

From within the `lesson-six` repo:

```
    cd slides
    reveal-md CLASS.md --theme melbdjango
```

[gh-fork]: https://help.github.com/articles/fork-a-repo/
[gh-pr]: https://help.github.com/articles/using-pull-requests/
[dj-request-response]: https://docs.djangoproject.com/en/1.8/ref/request-response/
[mdn-html]: https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Introduction
