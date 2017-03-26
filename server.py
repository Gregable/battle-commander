#!/usr/bin/env python

import BaseHTTPServer
import os
import signal
import argparse

ROOT = os.path.dirname(os.path.realpath(__file__))
cmd_args = None

COMMANDER = os.path.join(ROOT, 'commander.html')
VIEWER    = os.path.join(ROOT, 'viewer.html')

# This serves 3 HTML documents at:
# /commander - this is the hidden view for the DM with full data
# /viewer - this is the view shared with tabletop players with hidden data
# / - serves links to both of the above.

# There is also an endpoint at /shared 

global_SharedContents = "Click 'Start' from commander view"

class TransformingHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET(self):
    path = self.path
    if path == '/commander':
      self.Commander()
    elif path == '/viewer':
      self.Viewer()
    elif path == '/shared':
      self.Shared()
    else:
      # Serve a small set of links for easily opening the two docs.
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      self.wfile.write(
            """<a href="/commander">Commander</a><br>
               <a href="/viewer">Viewer</a><br><br>
               <a href="https://github.com/Gregable/battle-commander">
                 Gregable/battle-commander @ Github
               </a>
               """)

  def Commander(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()

    f = open(COMMANDER)
    contents = f.read()
    self.wfile.write(contents)

  def Viewer(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()

    f = open(VIEWER)
    contents = f.read()
    self.wfile.write(contents)

  def Shared(self):
    global global_SharedContents
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(global_SharedContents)

  def do_POST(self):
    global global_SharedContents
    if self.path != '/commander':
      return
    clength = int(self.headers.getheader('Content-Length'))
    global_SharedContents = self.rfile.read(clength)
    self.wfile.write('OK')

    if cmd_args.save_state:
      f = open(COMMANDER)
      contents = f.read()
      f.close()

      start = contents.find('<div id=container>') + len('<div id=container>')
      end = contents.find('</div id=container>')
      if start == -1 or end == -1:
        return
      # Replace contents with what was just posted to the server.
      newcontents = contents[:start] + global_SharedContents + contents[end:]

      f = open(COMMANDER, 'w')
      f.write(newcontents)
      f.close()


def SetUpSignalHandlers():
  def SignalHandler( signum, frame ):
    os._exit( 0 )

  for sig in { signal.SIGTERM, signal.SIGINT }:
    signal.signal( sig, SignalHandler )


def ParseArguments():
  parser = argparse.ArgumentParser()
  parser.add_argument( '--port', type = int, default = 8081,
                       help = 'The port to serve on.')
  parser.add_argument( '--host', type = str, default = '127.0.0.1',
                       help = 'The host to serve on.')
  parser.add_argument( '--save-state', type = bool, default = False,
                       help = 'If true, commander.html will be overwritten '
                       'with changes made in the browser. This is useful to '
                       'save state between encounters but not useful if '
                       'developing.' )

  args = parser.parse_args()
  return args


def Main():
  global cmd_args
  SetUpSignalHandlers()
  cmd_args = ParseArguments()

  httpd = BaseHTTPServer.HTTPServer(
    (cmd_args.host, cmd_args.port), TransformingHandler)
  print "serving at {}:{}".format(cmd_args.host, cmd_args.port)
  httpd.serve_forever()


if __name__ == '__main__':
  Main()
