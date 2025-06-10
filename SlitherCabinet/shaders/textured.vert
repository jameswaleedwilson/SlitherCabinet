#version 330 core

in vec3 vertices;
in vec3 vertex_color;
in vec3 vertex_normal;
in vec2 vertex_uv;
in vec2 vertex_texture;

uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;

out vec3 color;
out vec3 normal;
out vec3 frag_pos;
out vec3 view_pos;
out vec2 UV;
out vec2 text;

void main()
{

    view_pos = vec3(inverse(model_mat) * vec4(view_mat[3][0], view_mat[3][1], view_mat[3][2],1));

    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(vertices,1);

    normal = mat3(transpose(inverse(model_mat))) * vertex_normal;
    frag_pos = vec3(model_mat * vec4(vertices,1));
    color = vertex_color;
    UV = vertex_uv;
    text = vertex_texture;

}