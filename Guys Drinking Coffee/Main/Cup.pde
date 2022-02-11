class Cup {
  PVector pos;
  PVector current;


  float innerradius;
  float outerradius;
  float h;
  float coffeeHeigth;
  ArrayList<Smoke> smokes;
  public PShape shape;
  PImage texture, imgCat;

  public Cup() {
    this(0, 0, 0, null);
    current = new PVector();
  }
  
  public Cup(float innerradius, float outerradius, float h, PVector pos) {
    this.innerradius = innerradius;
    this.outerradius = outerradius;
    this.h = h;
    this.pos = pos;
    this.coffeeHeigth = h*0.1; // if h then empty if 0 then full
    this.smokes = new ArrayList<Smoke>();
    fillSmokes(smokes,new PVector(pos.x,pos.z));
    texture = loadImage("Marble.jpg");
    imgCat = loadImage("Cat.jpg");
    
    shape = createCylinder(20);
    shape.rotateY(-PI/2);
    shape.translate(pos.x, pos.y, pos.z);
  }

  void show(Guy g) {
    push();
    translate(0,map(sin(g.animation_time - PI/2), -1, 1, 0, -50),0);
    rotateX(map(sin(g.animation_time - PI/2), -1, 1, 0, PI/12));
    showSmokes(smokes,pos);
    pop();
  }
  
  void fillSmokes(ArrayList<Smoke> smokes,PVector pos){
    Smoke s;
    for (int i = 0; i < 20; i++) {
      s = new Smoke(pos);
      smokes.add(s);
    }
  }
  
  void showSmokes(ArrayList<Smoke> smokes,PVector pos){
  Smoke s;
  translate(pos.x,pos.y - (h+coffeeHeigth)  ,pos.z);
  for (int i = smokes.size() - 1; i >= 0; i--) {
        s = smokes.get(i);
        s.update();
        rotateY(radians(30));
        s.show();
        if (s.finished()) {
          smokes.remove(i);
          smokes.add(new Smoke(pos));
          
        }
      }
  }
  
  PShape createCylinder(int sides) {

    PShape cylinder = createShape(GROUP);

    float angle = 360 / sides;

    // draw top of the tube
    PShape top = createShape();
    top.beginShape(TRIANGLE_STRIP);
    top.noStroke();
    for (int i = 0; i < sides + 1; i++) {
      float x = cos( radians( i * angle ) );
      float y = sin( radians( i * angle ) );
      top.vertex(x * outerradius, 0, y * outerradius, i * texture.width/sides, 0);
      top.vertex(x * innerradius, 0, y * innerradius, i * texture.width/sides, texture.height);
    }
    top.endShape(CLOSE);
    top.setTexture(texture);

    cylinder.addChild(top);
    
    // draw coffee in the tube
    PShape coffee = createShape();
    coffee.beginShape();
    coffee.noStroke();
    for (int i = 0; i < sides; i++) {
      float x = cos( radians( i * angle ) );
      float y = sin( radians( i * angle ) );
      coffee.vertex(x * innerradius, coffeeHeigth, y * innerradius);
    }
    coffee.endShape(CLOSE);
    coffee.setFill(color(86,53,23));
    cylinder.addChild(coffee);

    // draw bottom of the tube
    PShape bottom = createShape();
    bottom.beginShape();
    bottom.noStroke();
    for (int i = 0; i < sides; i++) {
      float x = cos( radians( i * angle ) );
      float y = sin( radians( i * angle ) );
      bottom.vertex(x * outerradius, h, y * outerradius, i * texture.width/sides, texture.height);
    }

    bottom.endShape(CLOSE);
    bottom.setTexture(texture);
  //  Smoke(current.x, current.y);

    cylinder.addChild(bottom);

    // draw sides
    PShape middleout = createShape();
    middleout.beginShape(TRIANGLE_STRIP);
    middleout.noStroke();
    for (int i = 0; i < sides + 1; i++) {
      float x = cos( radians( 360 - i * angle ) );
      float y = sin( radians( 360 - i * angle ) );
      middleout.vertex( x * outerradius, 0, y*outerradius, i * imgCat.width/sides, 0);
      middleout.vertex( x * outerradius, h, y*outerradius, i * imgCat.width/sides, imgCat.height);
    }
    middleout.endShape(CLOSE);
    middleout.setTexture(imgCat);

    cylinder.addChild(middleout);

    PShape middlein = createShape();
    middlein.beginShape(TRIANGLE_STRIP);
    middlein.noStroke();
    for (int i = 0; i < sides + 1; i++) {
      float x = cos( radians( i * angle ) );
      float y = sin( radians( i * angle ) );
      middlein.vertex( x * innerradius, h, y*innerradius, i * texture.width/sides, 0);
      middlein.vertex( x * innerradius, 0, y*innerradius, i * texture.width/sides, texture.height);
    }
    middlein.endShape(CLOSE);
    middlein.setTexture(texture);

    cylinder.addChild(middlein);

    cylinder.addChild(createHolder());

    return cylinder;
  }

  PShape createHolder() {

    PShape handle = createShape(GROUP);

    float avg = (innerradius+outerradius)*0.45; 

    PShape top = createShape(BOX, h/5, h/10, avg);
    top.setTexture(texture);

    top.translate(0, 0.2*h, avg*1.55);
    handle.addChild(top);

    PShape bottom = createShape(BOX, h/5, h/10, avg);
    bottom.setTexture(texture);

    bottom.translate(0, 0.8*h, avg*1.55);
    handle.addChild(bottom);

    PShape mid = createShape(BOX, h/5, h/2, h/10);
    mid.setTexture(texture);
    
    mid.translate(0, 0.5*h, avg*2.05 - h/20);
    handle.addChild(mid);    
    return handle;
  }
}

class Smoke {
  float x, y, vx, vy,h, smoke_alpha;

  Smoke(PVector pos) {
    x = pos.x;
    y = pos.z;
    h = pos.y;
    vx = random(-0.25, 0.25);
    vy = random(-1, -0.5);
    smoke_alpha = 250;
  }

  boolean finished() {
    return smoke_alpha < 0;
  }

  void update() {
    x += vx;
    y += vy;
    smoke_alpha -= 10;
  }

  void show() {
    noStroke();
    fill(255, smoke_alpha);
    ellipse(x, y, 8, 8);
  }
}
