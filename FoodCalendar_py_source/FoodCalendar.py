"""well, this is the project at it stands now, truly there are, of course, further things to to,
an i did not even ad a nice icon, despite i already created one, but i know myself, if i dont say
to myself: "really thats it, i never gona launch and i allays find new things to do^^,
well it runs and i added all thins i thought of crucial, the rest will be for fun of for fame :D
things to do i already know of:
adding icons,
maybe sounds for finishing,
getting rid of the "google-not-trusted-Window"
increasing security, for my google-credentials as for the user as well
choosing conflicting appointments
a little DB for addresses,
or first of all an routine that prevents loading an address  a second time
AND a DB can cause trouble, if an company moves,
which, of course, is not very often, but non the less it happens sometime
well i now at nearly 30 hours for this project and it runs whit no bigger issues, and as i
thought of in the beginning...
what better moment to call it a day, so to speak"""
import randomone
import gui_toolkit

ding = randomone.SomethingDing()
if not ding.load():
    start_gui = gui_toolkit.Startframe()
    start_gui.pack()
    start_gui.mainloop()
    pass
else:
    one_two = ding.load()
    start_gui = gui_toolkit.Startframe(first=False, one_two=one_two)
    start_gui.pack()
    start_gui.mainloop()
    pass




