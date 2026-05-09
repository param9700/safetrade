import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;

public class SpaceShooter extends JPanel implements ActionListener, KeyListener {

    Timer timer;

    int playerX = 250;
    int playerY = 500;

    ArrayList<Rectangle> bullets = new ArrayList<>();
    ArrayList<Rectangle> enemies = new ArrayList<>();

    boolean left = false, right = false;

    public SpaceShooter() {
        timer = new Timer(20, this);
        timer.start();

        addKeyListener(this);
        setFocusable(true);

        // spawn enemies
        for (int i = 0; i < 5; i++) {
            enemies.add(new Rectangle(50 + i * 80, 50, 40, 40));
        }
    }

    public void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Background
        g.setColor(Color.BLACK);
        g.fillRect(0, 0, 600, 600);

        // Player
        g.setColor(Color.GREEN);
        g.fillRect(playerX, playerY, 50, 20);

        // Bullets
        g.setColor(Color.YELLOW);
        for (Rectangle b : bullets) {
            g.fillRect(b.x, b.y, b.width, b.height);
        }

        // Enemies
        g.setColor(Color.RED);
        for (Rectangle e : enemies) {
            g.fillRect(e.x, e.y, e.width, e.height);
        }
    }

    public void actionPerformed(ActionEvent e) {
        // Move player
        if (left && playerX > 0) playerX -= 5;
        if (right && playerX < 550) playerX += 5;

        // Move bullets
        for (int i = 0; i < bullets.size(); i++) {
            bullets.get(i).y -= 10;
        }

        // Collision detection
        for (int i = 0; i < bullets.size(); i++) {
            for (int j = 0; j < enemies.size(); j++) {
                if (bullets.get(i).intersects(enemies.get(j))) {
                    bullets.remove(i);
                    enemies.remove(j);
                    break;
                }
            }
        }

        repaint();
    }

    public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_LEFT) left = true;
        if (e.getKeyCode() == KeyEvent.VK_RIGHT) right = true;

        if (e.getKeyCode() == KeyEvent.VK_SPACE) {
            bullets.add(new Rectangle(playerX + 20, playerY, 5, 10));
        }
    }

    public void keyReleased(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_LEFT) left = false;
        if (e.getKeyCode() == KeyEvent.VK_RIGHT) right = false;
    }

    public void keyTyped(KeyEvent e) {}

    public static void main(String[] args) {
        JFrame frame = new JFrame("Space Shooter");
        SpaceShooter game = new SpaceShooter();

        frame.add(game);
        frame.setSize(600, 600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}