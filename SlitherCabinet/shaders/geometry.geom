#version 330 core
// https://learnopengl.com/Advanced-OpenGL/Geometry-Shader
layout (lines) in;
layout (triangle_strip, max_vertices = 84) out;

in VS_OUT {
    float extrude;
} gs_in[];

uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;

out vec3 color;
out vec3 normal;
out vec3 frag_pos;
//out vec2 UV;

mat4 translation_matrix = mat4(vec4(1.0, 0.0, 0.0, 0.0),
                               vec4(0.0, 1.0, 0.0, 0.0),
                               vec4(0.0, 0.0, 1.0, 0.0),
                               vec4(0.0, 0.0, 0.0, 1.0));
                                  //  x,   y,   z

mat4 scale_matrix = mat4(vec4(1.0, 0.0, 0.0, 0.0),
                         vec4(0.0, 1.0, 0.0, 0.0),
                         vec4(0.0, 0.0, 1.0, 0.0),
                         vec4(0.0, 0.0, 0.0, 1.0));

mat4 rotate_z_matrix = mat4(vec4(1.0, 0.0, 0.0, 0.0),
                              vec4(0.0, 1.0, 0.0, 0.0),
                              vec4(0.0, 0.0, 1.0, 0.0),
                              vec4(0.0, 0.0, 0.0, 1.0));

vec4 FILAMENT[84] = vec4[](
vec4( -0.5 , 0.0 , 0.1 , 1.0 ),
vec4( 0.5 , 0.0 , 0.1 , 1.0 ),
vec4( 0.5 , -0.141421 , 0.070711 , 1.0 ),
vec4( -0.5 , -0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , -0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , -0.2 , 0.0 , 1.0 ),
vec4( -0.5 , -0.2 , -0.0 , 1.0 ),
vec4( 0.5 , -0.2 , 0.0 , 1.0 ),
vec4( 0.5 , -0.141421 , -0.070711 , 1.0 ),
vec4( -0.5 , -0.141421 , -0.070711 , 1.0 ),
vec4( 0.5 , 0.0 , -0.1 , 1.0 ),
vec4( 0.5 , -0.141421 , -0.070711 , 1.0 ),
vec4( -0.5 , 0.0 , -0.1 , 1.0 ),
vec4( 0.5 , 0.141421 , -0.070711 , 1.0 ),
vec4( 0.5 , 0.0 , -0.1 , 1.0 ),
vec4( -0.5 , 0.141421 , -0.070711 , 1.0 ),
vec4( 0.5 , 0.2 , 0.0 , 1.0 ),
vec4( 0.5 , 0.141421 , -0.070711 , 1.0 ),
vec4( -0.5 , 0.2 , -0.0 , 1.0 ),
vec4( -0.5 , -0.2 , -0.0 , 1.0 ),
vec4( -0.5 , 0.0 , -0.1 , 1.0 ),
vec4( -0.5 , 0.2 , -0.0 , 1.0 ),
vec4( 0.5 , 0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , 0.2 , 0.0 , 1.0 ),
vec4( -0.5 , 0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , 0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , 0.0 , 0.1 , 1.0 ),
vec4( 0.5 , 0.2 , 0.0 , 1.0 ),
vec4( 0.5 , 0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , -0.141421 , -0.070711 , 1.0 ),
vec4( -0.5 , 0.0 , 0.1 , 1.0 ),
vec4( 0.5 , -0.141421 , 0.070711 , 1.0 ),
vec4( -0.5 , -0.141421 , 0.070711 , 1.0 ),
vec4( -0.5 , -0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , -0.2 , 0.0 , 1.0 ),
vec4( -0.5 , -0.2 , -0.0 , 1.0 ),
vec4( -0.5 , -0.2 , -0.0 , 1.0 ),
vec4( 0.5 , -0.141421 , -0.070711 , 1.0 ),
vec4( -0.5 , -0.141421 , -0.070711 , 1.0 ),
vec4( -0.5 , -0.141421 , -0.070711 , 1.0 ),
vec4( -0.5 , 0.0 , -0.1 , 1.0 ),
vec4( 0.5 , 0.0 , -0.1 , 1.0 ),
vec4( -0.5 , 0.0 , -0.1 , 1.0 ),
vec4( -0.5 , 0.141421 , -0.070711 , 1.0 ),
vec4( 0.5 , 0.141421 , -0.070711 , 1.0 ),
vec4( -0.5 , 0.141421 , -0.070711 , 1.0 ),
vec4( -0.5 , 0.2 , -0.0 , 1.0 ),
vec4( 0.5 , 0.2 , 0.0 , 1.0 ),
vec4( -0.5 , -0.2 , -0.0 , 1.0 ),
vec4( -0.5 , 0.0 , 0.1 , 1.0 ),
vec4( -0.5 , -0.141421 , 0.070711 , 1.0 ),
vec4( -0.5 , 0.0 , 0.1 , 1.0 ),
vec4( -0.5 , 0.2 , -0.0 , 1.0 ),
vec4( -0.5 , 0.141421 , 0.070711 , 1.0 ),
vec4( -0.5 , 0.2 , -0.0 , 1.0 ),
vec4( -0.5 , 0.0 , -0.1 , 1.0 ),
vec4( -0.5 , 0.141421 , -0.070711 , 1.0 ),
vec4( -0.5 , 0.0 , -0.1 , 1.0 ),
vec4( -0.5 , -0.2 , -0.0 , 1.0 ),
vec4( -0.5 , -0.141421 , -0.070711 , 1.0 ),
vec4( -0.5 , -0.2 , -0.0 , 1.0 ),
vec4( -0.5 , 0.2 , -0.0 , 1.0 ),
vec4( -0.5 , 0.0 , 0.1 , 1.0 ),
vec4( -0.5 , 0.2 , -0.0 , 1.0 ),
vec4( 0.5 , 0.141421 , 0.070711 , 1.0 ),
vec4( -0.5 , 0.141421 , 0.070711 , 1.0 ),
vec4( -0.5 , 0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , 0.0 , 0.1 , 1.0 ),
vec4( -0.5 , 0.0 , 0.1 , 1.0 ),
vec4( 0.5 , 0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , -0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , 0.0 , 0.1 , 1.0 ),
vec4( 0.5 , -0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , 0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , -0.2 , 0.0 , 1.0 ),
vec4( 0.5 , -0.2 , 0.0 , 1.0 ),
vec4( 0.5 , 0.141421 , 0.070711 , 1.0 ),
vec4( 0.5 , -0.141421 , -0.070711 , 1.0 ),
vec4( 0.5 , -0.141421 , -0.070711 , 1.0 ),
vec4( 0.5 , 0.0 , -0.1 , 1.0 ),
vec4( 0.5 , 0.141421 , -0.070711 , 1.0 ),
vec4( 0.5 , 0.141421 , -0.070711 , 1.0 ),
vec4( 0.5 , 0.2 , 0.0 , 1.0 ),
vec4( 0.5 , -0.141421 , -0.070711 , 1.0 ));

vec3 FILAMENT_NORMALS[84] = vec3[](
vec3( -0.0 , 0.2028 , -0.9792 ),
vec3( -0.0 , 0.2028 , -0.9792 ),
vec3( -0.0 , 0.2028 , -0.9792 ),
vec3( -0.0 , 0.7701 , -0.638 ),
vec3( -0.0 , 0.7701 , -0.638 ),
vec3( -0.0 , 0.7701 , -0.638 ),
vec3( -0.0 , 0.7701 , 0.638 ),
vec3( -0.0 , 0.7701 , 0.638 ),
vec3( -0.0 , 0.7701 , 0.638 ),
vec3( -0.0 , -0.2028 , -0.9792 ),
vec3( -0.0 , -0.2028 , -0.9792 ),
vec3( -0.0 , -0.2028 , -0.9792 ),
vec3( -0.0 , 0.2028 , -0.9792 ),
vec3( -0.0 , 0.2028 , -0.9792 ),
vec3( -0.0 , 0.2028 , -0.9792 ),
vec3( -0.0 , 0.7701 , -0.638 ),
vec3( -0.0 , 0.7701 , -0.638 ),
vec3( -0.0 , 0.7701 , -0.638 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( -0.0 , 0.7701 , 0.638 ),
vec3( -0.0 , 0.7701 , 0.638 ),
vec3( -0.0 , 0.7701 , 0.638 ),
vec3( -0.0 , -0.2028 , -0.9792 ),
vec3( -0.0 , -0.2028 , -0.9792 ),
vec3( -0.0 , -0.2028 , -0.9792 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( -0.0 , 0.2028 , -0.9792 ),
vec3( -0.0 , 0.2028 , -0.9792 ),
vec3( -0.0 , 0.2028 , -0.9792 ),
vec3( -0.0 , 0.7701 , -0.638 ),
vec3( -0.0 , 0.7701 , -0.638 ),
vec3( -0.0 , 0.7701 , -0.638 ),
vec3( -0.0 , 0.7701 , 0.638 ),
vec3( -0.0 , 0.7701 , 0.638 ),
vec3( -0.0 , 0.7701 , 0.638 ),
vec3( -0.0 , -0.2028 , -0.9792 ),
vec3( -0.0 , -0.2028 , -0.9792 ),
vec3( -0.0 , -0.2028 , -0.9792 ),
vec3( -0.0 , 0.2028 , -0.9792 ),
vec3( -0.0 , 0.2028 , -0.9792 ),
vec3( -0.0 , 0.2028 , -0.9792 ),
vec3( -0.0 , 0.7701 , -0.638 ),
vec3( -0.0 , 0.7701 , -0.638 ),
vec3( -0.0 , 0.7701 , -0.638 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( -0.0 , -0.7701 , -0.638 ),
vec3( -0.0 , -0.7701 , -0.638 ),
vec3( -0.0 , -0.7701 , -0.638 ),
vec3( -0.0 , -0.2028 , -0.9792 ),
vec3( -0.0 , -0.2028 , -0.9792 ),
vec3( -0.0 , -0.2028 , -0.9792 ),
vec3( -1.0 , -0.0 , -0.0 ),
vec3( -1.0 , -0.0 , -0.0 ),
vec3( -1.0 , -0.0 , -0.0 ),
vec3( -1.0 , -0.0 , -0.0 ),
vec3( -1.0 , -0.0 , -0.0 ),
vec3( -1.0 , -0.0 , -0.0 ),
vec3( -1.0 , -0.0 , -0.0 ),
vec3( -1.0 , -0.0 , -0.0 ),
vec3( -1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ),
vec3( 1.0 , -0.0 , -0.0 ));

void main()
{
    if (gs_in[1].extrude > float(0.0)) {

        // SCALE LENGTH
        // find distance between points
        float distance = float(distance(gl_in[0].gl_Position, gl_in[1].gl_Position));

        // update distance to scale matrix
        scale_matrix[0][0] = float(distance);

        // scale filament vertices
        for(int scale = 0; scale < 84; scale++) {
            FILAMENT[scale] = scale_matrix * FILAMENT[scale];
            //FILAMENT_NORMALS[scale] = vec3(scale_matrix * vec4(FILAMENT_NORMALS[scale], 1));
        }

        // ROTATE
        // find angle of z rotation from vector (1, 0, 0) in range of 0 to 360 degrees
        vec2 point1 = vec2(gl_in[0].gl_Position[0], gl_in[0].gl_Position[1]);
        vec2 point2 = vec2(gl_in[1].gl_Position[0], gl_in[1].gl_Position[1]);
        vec2 V1 = vec2(point2 - point1);
        float angle_z;

        // 1st quadrant
        if (V1[0] >= 0 && V1[1] >= 0) {
            angle_z = float(degrees(atan(V1[1] / V1[0])));
        }
        // 2nd quadrant
        else if (V1[0] < 0 && V1[1] > 0) {
            angle_z = float((degrees(atan(abs(V1[0]) / V1[1]))) + 90);
        }
        // 3rd quadrant
        else if (V1[0] <= 0 && V1[1] <= 0) {
            angle_z = float((degrees(atan(abs(V1[1]) / abs(V1[0])))) + 180);
        }
        // 4th quadrant
        else if (V1[0] > 0 && V1[1] < 0) {
            angle_z = float((degrees(atan(V1[0] / abs(V1[1])))) + 270);
        }

        // update angle_z to rotation matrix
        rotate_z_matrix[0][0] = float(cos(radians(angle_z)));
        rotate_z_matrix[1][1] = float(cos(radians(angle_z)));
        rotate_z_matrix[0][1] = float(sin(radians(angle_z)));
        rotate_z_matrix[1][0] = float(sin(radians(angle_z)) * -1);

        // rotate filament vertices around the z axis
        for(int rotate = 0; rotate < 84; rotate++) {
            FILAMENT[rotate] = rotate_z_matrix * FILAMENT[rotate];
            //FILAMENT_NORMALS[rotate] = vec3(rotate_z_matrix * vec4(FILAMENT_NORMALS[rotate], 1));
        }

        // TRANSLATE
        // find midpoint of two points
        vec4 midpoint = vec4((gl_in[0].gl_Position[0] + gl_in[1].gl_Position[0]) / 2,
                             (gl_in[0].gl_Position[1] + gl_in[1].gl_Position[1]) / 2,
                            ((gl_in[0].gl_Position[2] + gl_in[1].gl_Position[2]) / 2) - 0.1,
                                                                                   1);
        // update midpoint to translation matrix
        translation_matrix[3][0] = float(midpoint[0]);
        translation_matrix[3][1] = float(midpoint[1]);
        translation_matrix[3][2] = float(midpoint[2]);
        
        // translate filament vertices
        for(int translate = 0; translate < 84; translate++) {
            FILAMENT[translate] = translation_matrix * FILAMENT[translate];
        }

        // DRAW
        // draw vertices
        for(int vertices = 0; vertices < 84; vertices++) {
            color = vec3(1.0, 0.7, 0.0);
            frag_pos = vec3(FILAMENT[vertices]);
            normal = vec3(FILAMENT_NORMALS[vertices]);
            gl_Position = vec4(projection_mat * inverse(view_mat) * model_mat * FILAMENT[vertices]);
            EmitVertex();
        }

    }
        EndPrimitive();
}