#!/usr/bin/env python3
# -*- encoding: utf-8

import hashlib
import os
import plistlib
import shutil
import tempfile
import uuid

from PIL import Image
import yaml


class AlfredWorkflow:

    def __init__(self, path):
        self.path = path
        self.yaml_data = yaml.load(open(path))
        self.tmpdir = tempfile.mkdtemp()
        self.metadata = {}
        self.idx = 0

    def tmpfile(self, path):
        return os.path.join(self.tmpdir, path)

    def _construct_all_metadata(self):
        self.metadata = self._get_package_metadata()

        for link_data in self.yaml_data['links']:
            self._add_link(**link_data)

        for owner, repo_list in self.yaml_data.get('github', {}).items():
            for repo in repo_list:
                if isinstance(repo, str):
                    repo_name = repo
                    shortcut = repo
                else:
                    repo_name = repo['name']
                    shortcut = repo['shortcut']

                self._add_link(
                    url=f'https://github.com/{owner}/{repo_name}',
                    title=f'{owner}/{repo_name}',
                    icon='github.png',
                    shortcut=shortcut
                )

                if (
                    owner == 'wellcometrust' and
                    repo_name.startswith(('platform-', 'scala-'))
                ):
                    self._add_link(
                        url=f'https://github.com/{owner}/{repo_name}',
                        title=f'{owner}/{repo_name}',
                        icon='github.png',
                        shortcut=repo_name.split('-', 1)[1]
                    )

        for service in self.yaml_data.get('aws', []):
            name = service['name']
            shortcut = service.get('shortcut', name.lower())
            url = service.get('url', f'https://eu-west-1.console.aws.amazon.com/{shortcut}')

            self._add_link(
                url=url,
                title=name,
                icon=f'{shortcut}.png',
                shortcut=shortcut
            )

        for service in self.yaml_data['boto3']:
            name = service['name']
            slug = service.get('slug', name).lower()

            self._add_link(
                url=f'https://boto3.readthedocs.io/en/stable/reference/services/{slug}.html',
                title=f'boto3 docs for {name}',
                icon='boto3.png',
                shortcut=name.lower()
            )

        for iterm_shortcut in self.yaml_data['iterm2']:
            title = iterm_shortcut['title']
            shortcut = iterm_shortcut['shortcut']
            command = iterm_shortcut['command']

            trigger_object = {
                'config': {
                    'argumenttype': 2,
                    'keyword': shortcut,
                    'subtext': '',
                    'text': title,
                    'withspace': False,
                },
                'type': 'alfred.workflow.input.keyword',
                'uid': self.uuid('title', shortcut, title),
                'version': 1,
            }

            browser_object = {
                'config': {
                    'applescript': '\n'.join([
                        'on alfred_script(q)',
                        'tell application "iTerm" to create window with default profile command "%s"' % command,
                        'end alfred_script',
                    ]),
                    'cachescript': False,
                },
                'type': 'alfred.workflow.action.applescript',
                'uid': self.uuid('command', shortcut, command),
                'version': 1,
            }

            self._add_trigger_action_pair(
                trigger_object=trigger_object,
                action_object=browser_object,
                icon='iterm.png'
            )

        for journey in self.yaml_data.get('trains', []):
            t_from = journey['from']
            t_to = journey['to']

            self._add_link(
                url=f'https://www.thetrainline.com/train-times/{t_from.lower()}-to-{t_to.lower()}',
                title=f'Trains from {t_from} to {t_to}',
                icon='train-emoji.png',
                shortcut=f'{t_from.lower()} to {t_to.lower()}'
            )

        self._add_link(
            url='https://www.fastmail.com/mail/',
            title='FastMail',
            icon='fastmail.png',
            shortcut='fastmail'
        )

        for service in self.yaml_data['fastmail']:
            self._add_link(
                url=f'https://www.fastmail.com/{service.lower()}',
                title=f'{service} (FastMail)',
                icon='fastmail.png',
                shortcut=service.lower()
            )

        for command in self.yaml_data['python']:
            title = command['title']
            shortcut = command['shortcut']

            trigger_object = {
                'config': {
                    'argumenttype': 2,
                    'keyword': shortcut,
                    'subtext': '',
                    'text': title,
                    'withspace': False,
                },
                'type': 'alfred.workflow.input.keyword',
                'uid': self.uuid('shortcut', shortcut, title),
                'version': 1,
            }

            script_body = (
                open(os.path.join('scripts', command['file']))
                    .read()
                    .replace('#!/usr/bin/env python\n# -*- encoding: utf-8\n', '')
                    .strip()
            )

            script_object = {
                'config': {
                    'concurrently': False,
                    'escaping': 102,
                    'script': script_body,
                    'scriptargtype': 1,
                    'scriptfile': '',
                    'type': 3
                },
                'type': 'alfred.workflow.action.script',
                'uid': self.uuid('script', script_body),
                'version': 2,
            }

            self._add_trigger_action_pair(
                trigger_object=trigger_object,
                action_object=script_object,
                icon=command.get('icon', 'iterm.png')
            )

        for command in self.yaml_data['applescript']:
            title = command['title']
            shortcut = command['shortcut']

            trigger_object = {
                'config': {
                    'argumenttype': 2,
                    'keyword': shortcut,
                    'subtext': '',
                    'text': title,
                    'withspace': False,
                },
                'type': 'alfred.workflow.input.keyword',
                'uid': self.uuid('shortcut', shortcut, title),
                'version': 1,
            }

            script_body = (
                open(os.path.join('scripts', command['file']))
                    .read()
                    .strip()
            )

            script_object = {
                'config': {
                    'applescript': '\n'.join([
                        'on alfred_script(q)',
                        script_body,
                        'end alfred_script',
                    ]),
                    'cachescript': False,
                },
                'type': 'alfred.workflow.action.applescript',
                'uid': self.uuid('script', script_body),
                'version': 1,
            }

            self._add_trigger_action_pair(
                trigger_object=trigger_object,
                action_object=script_object,
                icon=command.get('icon', 'iterm.png')
            )

    def _copy_workflow_icon(self):
        try:
            icon = self.yaml_data['icon']
        except KeyError:
            pass
        else:
            icon_path = os.path.join('icons', icon)
            shutil.copyfile(icon_path, self.tmpfile('Icon.png'))

    def _get_package_metadata(self):
        defaults = {
            'bundleid': 'edu.self.alfred-junk-drawer',
            'category': 'Internet',
            'connections': {},
            'createdby': '',
            'description': 'An assorted collection of useful shortcuts for Alfred',
            'name': 'Alfred junk drawer',
            'objects': [],
            'readme': '',
            'uidata': {},
            'version': '0.0.1',
            'webaddress': 'https://github.com/alexwlchan/junkdrawer',
        }

        return {
            key: self.yaml_data.get(key, defaults[key]) for key in defaults
        }

    def _add_link(self, url, title, icon, shortcut):
        trigger_object = {
            'config': {
                'argumenttype': 0 if r'{query}' in url else 2,
                'keyword': shortcut,
                'subtext': '',
                'text': title,
                'withspace': (r'{query}' in url),
            },
            'type': 'alfred.workflow.input.keyword',
            'uid': self.uuid('link', shortcut, url),
            'version': 1,
        }

        browser_object = {
            'config': {
                'browser': '',
                'spaces': '',
                'url': url,
                'utf8': True,
            },
            'type': 'alfred.workflow.action.openurl',
            'uid': self.uuid('openurl', shortcut, url),
            'version': 1,
        }

        self._add_trigger_action_pair(
            trigger_object=trigger_object,
            action_object=browser_object,
            icon=icon
        )

    def uuid(self, *args):
        assert len(args) > 0
        md5 = hashlib.md5()
        for a in args:
            md5.update(a.encode('utf8'))

        # Quick check we don't have colliding UUIDs.
        if not hasattr(self, '_md5s'):
            self._md5s = {}
        hex_digest = md5.hexdigest()
        assert hex_digest not in self._md5s, (args, self._md5s[hex_digest])
        self._md5s[hex_digest] = args

        return str(uuid.UUID(hex=hex_digest)).upper()

    def _add_trigger_action_pair(self,
                                 trigger_object,
                                 action_object,
                                 icon):
        resized = self._resize_icon(icon)
        shutil.copyfile(resized, self.tmpfile(f'{trigger_object["uid"]}.png'))

        self.metadata['objects'].append(trigger_object)
        self.metadata['objects'].append(action_object)

        self.metadata['uidata'][trigger_object['uid']] = {
            'xpos': 150,
            'ypos': 50 + 120 * self.idx,
        }
        self.metadata['uidata'][action_object['uid']] = {
            'xpos': 600,
            'ypos': 50 + 120 * self.idx,
        }
        self.idx += 1

        self.metadata['connections'][trigger_object['uid']] = [
            {
                'destinationuid': action_object['uid'],
                'modifiers': 0,
                'modifiersubtext': '',
                'vitoclose': False,
            }
        ]

    def _resize_icon(self, filename):
        """
        Alfred icons have to be square, or they get blown up to fit the
        space, regardless of original aspect ratio.  This method puts icons
        on a square background with transparency, if necessary, to avoid
        this ugly resizing.
        """
        original = os.path.join('icons', filename)

        # We cache resized icons in .icons to avoid rebuilding them more
        # than necessary.
        resized = os.path.join('.icons', filename)
        os.makedirs('.icons', exist_ok=True)

        should_rebuild = (
            not os.path.exists(resized) or
            os.path.getmtime(resized) < os.path.getmtime(original)
        )

        if should_rebuild:
            base_icon = Image.open(original)
            width, height = base_icon.size
            if width == height:
                shutil.copyfile(original, resized)
            elif width > height:
                new = Image.new('RGBA', (width, width))
                new.paste(base_icon, (0, (width - height) // 2), base_icon)
                new.save(resized)
            else:
                new = Image.new('RGBA', (height, height))
                new.paste(base_icon, ((height - width) // 2, 0), base_icon)
                new.save(resized)

        return resized

    def _build_alfred_workflow_zip(self, name):
        """
        Given a directory of source files for an Alfred Workflow, assemble them
        into a .alfredworkflow bundle.
        """
        shutil.make_archive(
            base_name=f'{name}.alfredworkflow',
            format='zip',
            root_dir=self.tmpdir
        )
        shutil.move(f'{name}.alfredworkflow.zip', f'{name}.alfredworkflow')

    def assemble_package(self, name):
        self._construct_all_metadata()
        self._copy_workflow_icon()
        plistlib.writePlist(self.metadata, self.tmpfile('Info.plist'))
        self._build_alfred_workflow_zip(name=name)


def bump_version(path):
    existing_lines = list(open(path))
    assert existing_lines[3].startswith("version:")

    existing_version = int(existing_lines[3].split()[1])
    new_version = existing_version + 1
    existing_lines[3] = "version: %d\n" % (new_version + 1)

    with open(path, "w") as outfile:
        outfile.write("".join(existing_lines))


if __name__ == '__main__':
    bump_version("alfred_shortcuts.yml")
    workflow = AlfredWorkflow(path='alfred_shortcuts.yml')
    workflow.assemble_package(name='junkdrawer')
