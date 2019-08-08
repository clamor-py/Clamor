import unittest

from anyio import run
from clamor import Emitter, Priority


class TestEmitter(unittest.TestCase):

    def test_main_functionality(self):
        async def main():
            emitter = Emitter()
            goal = []

            async def early():
                goal.append(1)

            async def timely():
                goal.append(2)

            async def lately():
                goal.append(3)

            emitter.add_listener("test", early, Priority.BEFORE)
            emitter.add_listener("test", timely)
            emitter.add_listener("test", lately, Priority.AFTER)
            for _ in range(20):  # Make sure it wasn't an accident
                await emitter.emit("test")
                self.assertEqual(goal, [1, 2, 3])
                goal.clear()

        run(main)

    def test_removal(self):
        async def main():
            emitter = Emitter()
            goal = []

            async def early():
                goal.append(1)

            async def timely():
                goal.append(2)

            async def lately():
                goal.append(3)

            emitter.add_listener("test", early, Priority.BEFORE)
            emitter.add_listener("test", timely)
            emitter.add_listener("test", lately, Priority.AFTER)
            await emitter.emit("test")
            self.assertEqual(len(goal), 3)
            goal.clear()
            emitter.remove_listener("test", early)
            await emitter.emit("test")
            self.assertEqual(len(goal), 2)
            emitter.clear_event("test")
            self.assertFalse(emitter.listeners['test'])

        run(main)
