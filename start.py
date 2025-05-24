import os
import sys 
from modules.setup import SetUp
import asyncio

from app.services.args import Args


def run_ui():
    from ui.ui import build_ui
    ui = build_ui()
    ui.run(
         title="NAIR Admin Panel",
         host="127.0.0.1",
         port=8080,
         reload=True
    )



async def main():
   su = SetUp()
   await su()


if __name__ == "__main__":
   root = os.path.dirname(os.path.abspath(__file__))
   sys.path.append(root)
   os.chdir(root)

   args = Args()
   if args.ui_enabled():
         from ui.ui import build_ui
         ui = build_ui()
         ui.run(
            title="NAIR Admin Panel",
            host=args.host(),
            port=args.port(),
            reload=args.is_debug()
         )

   else:
      asyncio.run(main())