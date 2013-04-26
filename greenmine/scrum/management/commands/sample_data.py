# -*- coding: utf-8 -*-

import random
import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now

from django.contrib.webdesign import lorem_ipsum

from greenmine.base.models import User, Role
from greenmine.scrum.models import *
from greenmine.questions.models import *

subjects = [
    "Fixing templates for Django 1.2.",
    "get_actions() does not check for 'delete_selected' in actions",
    "Experimental: modular file types",
    "Add setting to allow regular users to create folders at the root level.",
    "add tests for bulk operations",
    "create testsuite with matrix builds",
    "Lighttpd support",
    "Lighttpd x-sendfile support",
    "Added file copying and processing of images (resizing)",
    "Exception is thrown if trying to add a folder with existing name",
    "Feature/improved image admin",
    "Support for bulk actions",
]


class Command(BaseCommand):
    def create_user(self, counter):
        user = User.objects.create(
            username='user%d' % (counter),
            first_name='user%d' % (counter),
            email='foouser%d@domain.com' % (counter),
            token=''.join(random.sample('abcdef0123456789', 10)),
        )

        user.set_password('user%d' % (counter))
        user.save()
        return user

    @transaction.commit_on_success
    def handle(self, *args, **options):
        users = [User.objects.get(is_superuser=True)]
        for x in range(10):
            users.append(self.create_user(x))

        role = Role.objects.all()[0]

        # projects
        for x in xrange(3):
            # create project
            project = Project(
                name='Project Example 1 %s' % (x),
                description='Project example %s description' % (x),
                owner=random.choice(users),
                public=True,
            )

            project.save()

            for user in users:
                Membership.objects.create(project=project, role=role, user=user)

            now_date = now() - datetime.timedelta(30)

            # create random milestones
            for y in xrange(2):
                milestone = Milestone.objects.create(
                    project=project,
                    name='Sprint %s' % (y),
                    owner=project.owner,
                    created_date=now_date,
                    modified_date=now_date,
                    estimated_start=now_date,
                    estimated_finish=now_date + datetime.timedelta(15),
                    order=10
                )

                now_date = now_date + datetime.timedelta(15)

                # create uss asociated to milestones
                for z in xrange(5):
                    us = UserStory.objects.create(
                        subject=lorem_ipsum.words(random.randint(4, 9), common=False),
                        project=project,
                        owner=random.choice(users),
                        description=lorem_ipsum.words(30, common=False),
                        milestone=milestone,
                        status=UserStoryStatus.objects.get(project=project, order=2),
                        points=Points.objects.get(project=project, order=3),
                        tags=[]
                    )

                    for tag in lorem_ipsum.words(random.randint(1, 5), common=True).split(" "):
                        us.tags.append(tag)

                    us.save()

                    for w in xrange(3):
                        Task.objects.create(
                            subject="Task %s" % (w),
                            description=lorem_ipsum.words(30, common=False),
                            project=project,
                            owner=random.choice(users),
                            milestone=milestone,
                            user_story=us,
                            status=TaskStatus.objects.get(project=project, order=4),
                        )

            # created unassociated uss.
            for y in xrange(10):
                us = UserStory.objects.create(
                    subject=lorem_ipsum.words(random.randint(4, 9), common=False),
                    status=UserStoryStatus.objects.get(project=project, order=2),
                    points=Points.objects.get(project=project, order=3),
                    owner=random.choice(users),
                    description=lorem_ipsum.words(30, common=False),
                    milestone=None,
                    project=project,
                    tags=[],
                )

                for tag in lorem_ipsum.words(random.randint(1, 5), common=True).split(" "):
                    us.tags.append(tag)

                us.save()

            # create bugs.
            for y in xrange(20):
                bug = Issue.objects.create(
                    project=project,
                    subject=lorem_ipsum.words(random.randint(1, 5), common=False),
                    description=lorem_ipsum.words(random.randint(1, 15), common=False),
                    owner=project.owner,
                    severity=Severity.objects.get(project=project, order=2),
                    status=IssueStatus.objects.get(project=project, order=4),
                    priority=Priority.objects.get(project=project, order=3),
                    type=IssueType.objects.get(project=project, order=1),
                    tags=[],
                )

                for tag in lorem_ipsum.words(random.randint(1, 5), common=True).split(" "):
                    bug.tags.append(tag)

                bug.save()

            # create questions.
            for y in xrange(20):
                question = Question.objects.create(
                    project=project,
                    subject=lorem_ipsum.words(random.randint(1, 5), common=False),
                    content=lorem_ipsum.words(random.randint(1, 15), common=False),
                    owner=project.owner,
                    status=QuestionStatus.objects.get(project=project, order=1),
                    tags=[],
                )

                for tag in lorem_ipsum.words(random.randint(1, 5), common=True).split(" "):
                    question.tags.append(tag)

                question.save()
