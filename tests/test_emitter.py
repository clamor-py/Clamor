import unittest

from clamor import Emitter, Priority

from anyio import run


class TestEmitter(unittest.TestCase):

    def test_main_functionality(self):
        async def main():
            emitter = Emitter()
            goal = []

            async def early(_):
                goal.append(1)

            async def timely(_):
                goal.append(2)

            async def late(_):
                goal.append(3)

            emitter.add_listener("test", early, Priority.BEFORE)
            emitter.add_listener("test", timely)
            emitter.add_listener("test", late, Priority.AFTER)
            for _ in range(20):  # Make sure it wasn't an accident
                await emitter.emit("test", {})
                self.assertEqual(goal, [1, 2, 3])
                goal.clear()
        run(main)

    def test_removal(self):
        async def main():
            emitter = Emitter()
            goal = []

            async def early(_):
                goal.append(1)

            async def timely(_):
                goal.append(2)

            emitter.add_listener("test", early, Priority.BEFORE)
            emitter.add_listener("test", early, Priority.BEFORE)
            emitter.add_listener("test", timely)
            await emitter.emit("test", {})
            self.assertEqual(len(goal), 3)
            goal.clear()
            emitter.remove_listener("test", early)
            await emitter.emit("test", {})
            self.assertEqual(len(goal), 1)
            emitter.clear_event("test")
            self.assertFalse(emitter.listeners['test'])
