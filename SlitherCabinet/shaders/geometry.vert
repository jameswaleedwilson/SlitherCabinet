#version 430 core

layout (location = 0) in vec4 points;

uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;

out VS_OUT {
    float extrude;
} vs_out;

void main() {

    gl_Position = vec4(points[0], points[1], points[2], 1);

    vs_out.extrude = points[3];

}