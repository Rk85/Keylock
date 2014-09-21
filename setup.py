from distutils.core import setup
import py2exe

setup(name="Keylock",
      windows=["src/Keylock.py"],
      package_dir = {'': 'src'},
      py_modules = ['clip_board_timer',
                    'file_menu',
                    'folders_panel',
                    'item_details_panel',
                    'folder_pop_menu',
                    'item_pop_menu',
                    'item_window',
                    'items_panel',
                    'Keylock',
                    'login',
                    'menu',
                    'settings',
                    'view_menu'
                    ],
      data_files=[("icons",
                   ["src/icons/about.png",
                    "src/icons/add_folder.png",
                    "src/icons/add_item.png",
                    "src/icons/copy_pass.png",
                    "src/icons/copy_user.png",
                    "src/icons/delete_folder.png",
                    "src/icons/delete_pass.png",
                    "src/icons/edit_pass.png",
                    "src/icons/exit.png",
                    "src/icons/expiry_time.png",
                    "src/icons/folder.png",
                    "src/icons/item.png",
                    "src/icons/new_file.png",
                    "src/icons/open.png",
                    "src/icons/save.png",
                    "src/icons/save_as.png",
                    "src/icons/short_icon.ico"
                    ]
                   ),
                  ('.', ['src/icons/short_cut.vbs'])
                  ]
)
