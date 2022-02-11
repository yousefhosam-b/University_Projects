class Background
{
  PImage imgGrass = loadImage("Grass.jpg");
  PImage imgSky = loadImage("Sky.jpg"); 
  PImage imgCeiling = loadImage("Ceiling.jpg");


  // Wanna draw a House ? :D
  class House
  {
    PImage imgWall = loadImage("Wall.jpg");
    PImage imgRoof = loadImage("Roof.jpg");
    PImage imgDoor = loadImage("Door.jpg");

    void drawHouse() 
    {
      drawStructure();
      drawRoof();
      drawDoor();
    }

    void drawStructure() 
    {
      int w = imgWall.width;
      int h = imgWall.height;
      pushMatrix();
      translate(1490, -500, 0);

      beginShape(QUADS);
      texture(imgWall);
      //+Z face
      vertex(-500, -500, 500, 0, 0); //top left 
      vertex( 500, -500, 500, w, 0); //top right
      vertex( 500, 500, 500, w, h); //bottom right 
      vertex(-500, 500, 500, 0, h); //bottom left 

      //-Z face
      vertex(-500, -500, -500, 0, 0); //top left 
      vertex(500, -500, -500, w, 0); //top right
      vertex(500, 500, -500, w, h); //bottom right 
      vertex(-500, 500, -500, 0, h); //bottom left 

      //+X face
      vertex(500, -500, 500, 0, 0); //top left 
      vertex(500, -500, -500, w, 0); //top right
      vertex(500, 500, -500, w, h); //bottom right 
      vertex(500, 500, 500, 0, h); //bottom left

      //-X face
      vertex(-500, -500, 500, 0, 0); //top left 
      vertex(-500, -500, -500, w, 0); //top right
      vertex(-500, 500, -500, w, h); //bottom right 
      vertex(-500, 500, 500, 0, h); //bottom left

      //-Y face
      vertex(-500, -500, 500, 0, 0); //top left  
      vertex( 500, -500, 500, w, 0); //top right 
      vertex( 500, -500, -500, w, h); //bottom right 
      vertex(-500, -500, -500, 0, h); //bottom left

      //+Y face
      vertex(-500, 500, 500, 0, 0); //top left  
      vertex( 500, 500, 500, w, 0); //top right 
      vertex( 500, 500, -500, w, h); //bottom right 
      vertex(-500, 500, -500, 0, h); //bottom left
      endShape();
      popMatrix();
    }

    void drawRoof()
    {
      int w = imgRoof.width;
      int h = imgRoof.height;
      pushMatrix();
      translate(1490, -750, 0);
      rotateY(radians(90));

      beginShape(QUADS);
      texture(imgRoof);
      vertex(-500, -250, 500, 0, 0);
      vertex( 500, -250, 500, w, 0);
      vertex( 500, -250, -500, w, h);
      vertex(-500, -250, -500, 0, h);

      vertex(  0, -500, 500, 0, 0);
      vertex(  0, -500, -500, w, 0);
      vertex(500, -250, -500, w, h);
      vertex(500, -250, 500, 0, h);

      vertex(   0, -500, 500, 0, 0);
      vertex(   0, -500, -500, w, 0);
      vertex(-500, -250, -500, w, h);
      vertex(-500, -250, 500, 0, h);
      endShape();

      beginShape(TRIANGLE);
      texture(imgRoof);
      vertex(-500, -250, 500, 0, h);
      vertex( 500, -250, 500, w, h);
      vertex(   0, -500, 500, w/2, 0);

      vertex(-500, -250, -500, 0, h);
      vertex( 500, -250, -500, w, h);
      vertex(   0, -500, -500, w/2, 0);
      endShape();
      popMatrix();
    }

    void drawDoor()
    {
      int w = imgDoor.width;
      int h = imgDoor.height;
      pushMatrix();
      translate(915, -300, 0);
      rotateZ(radians(76));

      beginShape(QUADS);
      texture(imgDoor);
      vertex(-300, -150, -300, 0, 0);
      vertex(-300, -150, 300, w, 0);
      vertex( 300, 0, 300, w, h);
      vertex( 300, 0, -300, 0, h);
      endShape();
      popMatrix();
    }
  }


  // Wanna draw a Tree ? :D
  class Tree
  {
    PImage imgBody = loadImage("Body.jpg");
    PImage imgLeaf = loadImage("Leaf.jpg");

    void drawTree() 
    {
      drawBody();
      drawLeaves();
    }

    void drawLeaves()
    {
      // draw Leaves
      int pieces = 36;  // you will shift 10 degrees each time
      int increaseAngle = 360 / pieces;
      int r = 600;
      int h = 1000;

      pushMatrix();
      translate(500, -500, 1300);
      beginShape(TRIANGLE_FAN);
      texture(imgLeaf);
      vertex(0, -h, 0, imgLeaf.width / 2, 0);
      for (int i = 0; i < pieces; i++)
      {
        vertex(r * cos(radians(i * increaseAngle)), 50, r * sin(radians(i * increaseAngle)), imgLeaf.width, imgLeaf.height);
        vertex(r * cos(radians((i + 1)*increaseAngle)), 50, r * sin(radians((i + 1)*increaseAngle)), 0, imgLeaf.height);
      }
      endShape();
      popMatrix();
    }

    void drawBody()
    {
      int pieces = 36;  // you will shift 10 degrees each time
      int increaseAngle = 360 / pieces;
      int r = 150;
      int h = 1200;
      int w = imgBody.width;

      pushMatrix();
      translate(500, -1200, 1300);
      beginShape(QUADS);
      texture(imgBody);
      for (int i = 0; i < pieces; i++)
      {
        vertex(r * cos(radians(i * increaseAngle)), 0, r * sin(radians(i * increaseAngle)), i * w / pieces, 0);
        vertex(r * cos(radians((i + 1)*increaseAngle)), 0, r * sin(radians((i + 1)*increaseAngle)), (i+1) * w / pieces, 0);
        vertex(r * cos(radians((i + 1)*increaseAngle)), h, r * sin(radians((i + 1)*increaseAngle)), (i+1) * w / pieces, imgBody.height);
        vertex(r * cos(radians(i * increaseAngle)), h, r * sin(radians(i * increaseAngle)), i * w / pieces, imgBody.height);
      }
      endShape();
      popMatrix();
    }
  }


  // Wanna draw a Bird ? :D
  class Bird 
  {
    float R, G, B, speed, z;
    float angle = 0;
    float flapSpeed = 0.2;

    public Bird()
    {
      initializeRandoms();
    }

    void initializeRandoms()
    {
      R = random(255);
      G = random(255);
      B = random(255);
      speed = random(3, 7);
      z = 2000;
    }

    void drawBird() {
      translate(-1000, -600, z);
      rotateX(radians(90));

      // Body
      fill(R, G, B);
      box(20, 100, 20);

      // Left wing
      pushMatrix();
      rotateY(sin(radians(angle)) * -20);
      rect(-75, -50, 75, 100);
      popMatrix();

      // Right wing
      pushMatrix();
      rotateY(sin(radians(angle)) * 20);
      rect(0, -50, 75, 100);
      popMatrix();

      // Head
      pushMatrix();
      noStroke();
      lights();
      specular(R, G, B);
      translate(0, -65, 0);
      sphere(25);
      popMatrix();

      // Tail
      pushMatrix();
      translate(-35, 30, 5);
      stroke(0);
      strokeWeight(2);
      line(30, 20, 75, 65);
      noStroke();
      lights();
      specular(R, G, B);
      translate(75, 70, 0);
      sphere(15);
      popMatrix();

      // Beak
      pushMatrix();
      fill(0);
      translate(0, -120, 0);

      beginShape(QUADS);
      // first side
      vertex(0, 0, 0);
      vertex(12.5, 35, 12.5);
      vertex(-12.5, 35, 12.5);

      // second side
      vertex(0, 0, 0);
      vertex(12.5, 35, 12.5);
      vertex(12.5, 35, -12.5);

      // third side
      vertex(0, 0, 0);
      vertex(-12.5, 35, 12.5);
      vertex(-12.5, 35, -12.5);

      // forth side
      vertex(0, 0, 0);
      vertex(12.5, 35, -12.5);
      vertex(-12.5, 35, -12.5);
      endShape();
      popMatrix();

      // Legs
      pushMatrix(); // first leg
      translate(0, 30, -10);
      stroke(0);
      strokeWeight(2);
      rotateY(radians(90));
      line(30, 20, -5, 5);
      popMatrix();

      pushMatrix(); // second leg
      translate(10, 10, -10);
      stroke(0);
      strokeWeight(2);
      rotateY(radians(90));
      line(30, 20, -5, 5);
      popMatrix();

      // Wing flap
      angle += flapSpeed;
      if (angle > 4) {
        flapSpeed *= -1;
      }
      if (angle < -4) {
        flapSpeed *= -1;
      }

      z -= speed; 
      if (z < -2000)
        initializeRandoms();
    }
  }

  void drawGrass()
  {
    int w = imgGrass.width;
    int h = imgGrass.height;

    beginShape(QUADS);
    texture(imgGrass);
    vertex(-2000, 1.000, 2000, 0, 0);
    vertex(2000, 1.000, 2000, w, 0);
    vertex(2000, 1.000, -2000, w, h);
    vertex(-2000, 1.000, -2000, 0, h);
    endShape();
  }

  void drawSky() 
  {
    int w = imgSky.width;
    int h = imgSky.height;

    beginShape(QUADS); // first view
    texture(imgSky);
    vertex(-2000, -2000, -2000, w, 0); // top left
    vertex(-2000, -2000, 2000, 0, 0); // top right 
    vertex(-2000, 0, 2000, 0, h); // bottom right 
    vertex(-2000, 0, -2000, w, h); // bottom left 
    endShape();

    beginShape(QUADS); // second view
    texture(imgSky);
    vertex(2000, -2000, -2000, 0, 0); // top left 
    vertex(2000, -2000, 2000, w, 0); // top right 
    vertex(2000, 0, 2000, w, h); // bottom right 
    vertex(2000, 0, -2000, 0, h); // bottom left 
    endShape();

    beginShape(QUADS); // third view
    texture(imgSky);
    vertex(-2000, -2000, 2000, 0, 0); // top left 
    vertex(2000, -2000, 2000, w, 0); // top right 
    vertex(2000, 0, 2000, w, h); // bottom right 
    vertex(-2000, 0, 2000, 0, h); // bottom left 
    endShape();

    beginShape(QUADS); // fourth view
    texture(imgSky);
    vertex(2000, -2000, -2000, 0, 0); // top left 
    vertex(-2000, -2000, -2000, w, 0); // top right 
    vertex(-2000, 0, -2000, w, h); // bottom right 
    vertex(2000, 0, -2000, 0, h); // bottom left 
    endShape();
  }

  void drawCeiling()
  {
    int w = imgCeiling.width;
    int h = imgCeiling.height;

    beginShape(QUADS);
    texture(imgCeiling);
    vertex(-2000, -2000, 2000, 0, 0);
    vertex(2000, -2000, 2000, w, 0);
    vertex(2000, -2000, -2000, w, h);
    vertex(-2000, -2000, -2000, 0, h);
    endShape();
  }
}
