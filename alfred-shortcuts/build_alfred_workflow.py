#!/usr/bin/env python3
# -*- encoding: utf-8

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

    def build(self, name):
        self.metadata = self._get_package_metadata()

        for link_data in self.yaml_data['links']:
            self._add_link(link_data=link_data)

        for owner, repo_list in self.yaml_data.get('github', {}).items():
            for repo_name in repo_list:
                self._add_link(link_data={
                    'title': f'{owner}/{repo_name}',
                    'icon': 'github.png',
                    'shortcut': repo_name,
                    'url': f'https://github.com/{owner}/{repo_name}'
                })

        for service in self.yaml_data.get('aws', []):
            title = service['title']
            shortcut = service.get('shortcut', title.lower())
            url = service.get('url', f'https://eu-west-1.console.aws.amazon.com/{shortcut}')
            self._add_link(link_data={
                'title': title,
                'icon': f'{shortcut}.png',
                'shortcut': shortcut,
                'url': url,
            })

        for service in self.yaml_data['boto3']:
            title = service['title']
            shortcut = service.get('shortcut', title.lower())
            slug = service.get('slug', title).lower()
            url = f'https://boto3.readthedocs.io/en/stable/reference/services/{slug}.html'
            self._add_link(link_data={
                'title': title,
                'icon': 'boto3.png',
                'shortcut': title.lower(),
                'url': url,
            })

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
                'uid': str(uuid.uuid4()).upper(),
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
                'uid': str(uuid.uuid4()).upper(),
                'version': 1,
            }

            self._add_trigger_action_pair(
                trigger_object=trigger_object,
                action_object=browser_object,
                icon_name='iterm.png'
            )

        for journey in self.yaml_data.get('trains', []):
            t_from = journey['from']
            t_to = journey['to']
            shortcut = f'{t_from.lower()} to {t_to.lower()}'
            url = f'https://www.thetrainline.com/train-times/{t_from.lower()}-to-{t_to.lower()}'
            self._add_link(link_data={
                'title': f'Trains from {t_from} to {t_to}',
                'icon': f'train-emoji.png',
                'shortcut': shortcut,
                'url': url,
            })

        self._copy_workflow_icon()
        plistlib.writePlist(self.metadata, self.tmpfile('Info.plist'))
        self._build_alfred_workflow_zip(name=name)

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

    def _add_link(self, link_data):
        shortcut = link_data['shortcut']
        url = link_data['url']
        title = link_data['title']

        trigger_object = {
            'config': {
                'argumenttype': 0 if r'{query}' in url else 2,
                'keyword': shortcut,
                'subtext': '',
                'text': title,
                'withspace': (r'{query}' in url),
            },
            'type': 'alfred.workflow.input.keyword',
            'uid': str(uuid.uuid4()).upper(),
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
            'uid': str(uuid.uuid4()).upper(),
            'version': 1,
        }

        self._add_trigger_action_pair(
            trigger_object=trigger_object,
            action_object=browser_object,
            icon_name=link_data['icon']
        )

    def _add_trigger_action_pair(self,
                                 trigger_object,
                                 action_object,
                                 icon_name):
        resized = self._resize_icon(icon_name)
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


if __name__ == '__main__':
    workflow = AlfredWorkflow(path='alfred_shortcuts.yml')
    workflow.build(name='junkdrawer')
