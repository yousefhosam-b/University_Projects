import peasy.*;
import processing.sound.*;

PeasyCam cam;
SoundFile file;
String audioName = "Nature.mp3";
String path;

void setup() {
  size(800, 600, P3D);
  cam = new PeasyCam(this, 550);
  path = sketchPath(audioName);
  file = new SoundFile(this, path);
  file.play();

  fill(255);

  bg = new Background();
  t1 = bg.new Tree();
  t2 = bg.new Tree();
  b = bg.new Bird();
  h = bg.new House();

  t = new Table(100, 200, 10, 80);
  c1 = new Chair(50, 75, 10, 50, 60);
  c2 = new Chair(50, 75, 10, 50, 60);

  cup1 = new Cup(15, 20, 50, new PVector(0, -140, 80));
  cup2 = new Cup(15, 20, 50, new PVector(-5, -140, 65));

  g1 = new Guy(50, 10, 50);
  g2 = new Guy(50, 10, 50);

  g1.ral.addChild(cup1.shape);  
  g2.ral.addChild(cup2.shape);

  ch = new Chat();
}

Background bg;
Background.Tree t1; 
Background.Tree t2; 
Background.Bird b;
Background.House h;
Table t;
Chair c1, c2;
Guy g1, g2;
Cup cup1, cup2;
Chat ch;


void draw() {
  clear();
  background(120);
  //directionalLight(255, 255, 255, 0.5, 1, 0.5);

  t.show();
  translate(0, 0, -150);
  c1.show();
  cup1.show(g1);
  g1.show();
  translate(0, 0, 300);
  rotateY(radians(180));
  c2.show();
  cup2.show(g2);
  g2.show();

  push();
  b.drawBird();
  pop();

  push();
  h.drawHouse();
  pop();

  push();
  t1.drawTree();
  translate(0, 0, -2600);
  t2.drawTree();
  pop();

  bg.drawGrass();
  bg.drawSky();
  // bg.drawCeiling

  push();
  rotateY(radians(90));
  translate(-500, -500, -500);
  ch.draw();
  pop();
}

void keyPressed() {
  clear();
  background(200); 
  if (keyCode == ENTER) {
    ch.current++;
    if (ch.current >= 14) {
      ch.current = 14 - 1;
    }
  }

  if (keyCode == BACKSPACE) {
    ch.current--;
    if (ch.current < 0) {
      ch.current = 0;
    }
  }
}
