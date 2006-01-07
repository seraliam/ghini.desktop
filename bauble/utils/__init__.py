#
# this is just a dummy file so i can import on this directory
#

import imp, os, sys, re
import gtk
import bauble

# TODO: if i escape the messages that come in then my own markup doesn't 
# work, what really needs to be done is make sure that any exception that
# are going to be passed to one of these dialogs should be escaped before 
# coming through

def message_dialog(msg, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK):
    if hasattr(bauble, "app"): # this might get called before bauble has started
        parent = bauble.app.gui.window
    else:
	parent = None	
    d = gtk.MessageDialog(flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
			  parent=bauble.app.gui.window,
                          type=type, buttons=buttons)
    d.set_markup(msg)
    r = d.run()
    d.destroy()
    return r
    

def yes_no_dialog(msg):
    if hasattr(bauble, "app"): # this might get called before bauble has started
	parent = bauble.app.gui.window
    else:
	parent = None
    d = gtk.MessageDialog(flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                          parent=bauble.app.gui.window,
			  type=gtk.MESSAGE_QUESTION,
                          buttons = gtk.BUTTONS_YES_NO)            
    d.set_markup(msg)    
    r = d.run()
    d.destroy()
    return r == gtk.RESPONSE_YES


def message_details_dialog(msg, details, type=gtk.MESSAGE_INFO, 
                           buttons=gtk.BUTTONS_OK):
    if hasattr(bauble, "app"): # this might get called before bauble has started
	    parent = bauble.app.gui.window
    else:
	parent = None
    d = gtk.MessageDialog(flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
			  parent=parent,
                          type=type, buttons=buttons)        
    d.set_markup(msg)
    expand = gtk.Expander("Details")    
    text_view = gtk.TextView()
    text_view.set_editable(False)
    text_view.set_wrap_mode(gtk.WRAP_WORD)
    tb = gtk.TextBuffer()
    tb.set_text(details)
    text_view.set_buffer(tb)
    sw = gtk.ScrolledWindow()
    sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    sw.add(text_view)    
    expand.add(sw)
    d.vbox.pack_start(expand)
    d.show_all()
    r = d.run()
    d.destroy() # TODO: should we be hiding or destroying
    return r


def startfile(filename):
    if sys.platform == 'win32':
        os.startfile(filename)
    elif sys.platform == 'linux2':
        # need to determine if gnome or kde
        os.system("gnome-open " + filename)
    else:
        raise Exception("bauble.utils.startfile(): can't open file:" + filename)
        

def dms_to_decimal(dir, deg, min, sec):
    """
    convert degrees, minutes, seconds to decimal
    """
    # TODO: more test cases
    dec = (((sec/60.0) + min) /60.0) + deg
    if dir == 'W' or dir == 'S':
        dec = -dec
    return dec
    
        
def decimal_to_dms(decimal, long_or_lat):
    """
    long_or_lat: should be either 'long' or 'lat'
    """
    # NOTE: if speed is an issue, which i don't think it ever will be
    # this could probably be optimized
    # TODO: more test cases
    dir_map = { 'long': ['E', 'W'],
                'lat':  ['N', 'S']}
    dir = dir_map[long_or_lat][1]
    if decimal < 0:
        dir = dir_map[long_or_lat][0]
        
    dec = abs(decimal)
    d = abs(int(dec))
    m = abs((dec-d)*60)
    s = abs((int(m)-m) * 60)
    return dir, int(d), int(m), int(s)
    
    
def longitude_to_dms(decimal):
    return decimal_to_dms(decimal, 'long')

    
def latitude_to_dms(decimal):
    return decimal_to_dms(decimal, 'lat')
   
    
if __name__ == '__main__':
    """
    could probably put this in a doctest
    """
    dec = dms_to_decimal('W', 87, 43, 41)
    dir, deg, min, sec = decimal_to_dms(dec, 'long')
    print dec
    print '%s %d %d %d' % (dir, deg, min, sec)
   
   
